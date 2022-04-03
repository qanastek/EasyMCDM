import numpy as np
from typing import Dict, List, Union
from collections import Counter

from EasyMCDM.models.MCDM import MCDM

class Electre(MCDM):
    
    # Memory allocation
    __slots__ = [
        'verbose', 
        'criteria', 
        'weights', 
        'preferences', 
    ]

    # Constructor
    def __init__(self, data : Union[str, dict], col_sep=',', row_sep='\n', verbose=True):
        super().__init__(data, col_sep=col_sep, row_sep=row_sep, verbose=verbose)

    def __print_electre__(
        self, 
        concordance_matrix, 
        non_discordance_matrix, 
        result_matrix, 
        kernels,
        robustness_analysis_results: dict,
        frequent_kernels: dict,
    ):
        for x in range(len(concordance_matrix)):
            print('\t'.join(["{:1.3f}".format(y) if y != 'x' else y for y in concordance_matrix[x]]))

        print()
        for x in range(len(non_discordance_matrix)):
            print('\t'.join(["{:1.3f}".format(y) if y != 'x' else y for y in non_discordance_matrix[x]]))

        print()
        for x in range(len(result_matrix)):
            print('\t'.join([str(y) for y in result_matrix[x]]))

        print()
        print(kernels)

        print()
        print('Robustness Analysis:')
        print('\n'.join(robustness_analysis_results))
        
        print()
        print('Most Frequent Kernels:')
        print(', '.join(frequent_kernels))
        return

    def __robustness_analysis__(self, concordance_matrix, non_discordance_matrix):
        robustness_analysis_kernels = {}
        for threshold in np.arange(0.5, 1.025, 0.025):
            # Compute outranking matrix from concordance and non-discordance
            outranking_matrix = self.__get_outranking_matrix__(
                concordance_matrix, non_discordance_matrix, threshold)

            # Compute the graph kernels
            robustness_analysis_kernels[threshold] = self.__get_kernels__(outranking_matrix)

        analysis_results = []
        ordered_candidates = []

        occurences = Counter()
        for key in robustness_analysis_kernels.keys():
            occurences.update(robustness_analysis_kernels[key])
            analysis_results.append(
                '[{:0.3f}] = {}'.format(key, ', '.join(robustness_analysis_kernels[key]))
            )
        
        ordered_candidates = ['{} ({})'.format(item, occ) for item, occ in occurences.most_common()]

        return (analysis_results, ordered_candidates)


    def __get_electre1_matrices__(self, weights, preferences, vetoes, preference_thresholds):
        size = len(self.names)

        concordance_matrix = [[0] * size for _ in range(size)]
        non_discordance_matrix = [[0] * size for _ in range(size)]

        data = list(self.matrix.values())

        for x in range(size):
            for y in range(x, size):
                if (x == y):
                    concordance_matrix[x][y] = non_discordance_matrix[x][y] = 'x'
                    continue
                
                a = data[x]
                b = data[y]
                av = bv = 0.0

                a_are_vetoes_respected = b_are_vetoes_respected = True
                for idx, (w, p, v) in enumerate(zip(weights, preferences, vetoes)):
                    best_val = 0
                    if (p == 'max'):
                        best_val = max(a[idx], b[idx])
                    else:
                        best_val = min(a[idx], b[idx])
                    
                    diff = abs(b[idx] - a[idx])
                    
                    # NOTE: ELECTRE I-v
                    points = 0.0 if diff != 0 else w

                    # NOTE: ELECTRE I-s
                    if (preference_thresholds != None):
                        pref_threshold = preference_thresholds[idx]
                        if (diff < pref_threshold):
                            points = (1 - (diff / pref_threshold)) * w

                    if (best_val == a[idx]):
                        av += w
                        bv += points
                        b_are_vetoes_respected = ((b_are_vetoes_respected) and diff < v)
                    else:
                        av += points
                        bv += w
                        a_are_vetoes_respected = ((a_are_vetoes_respected) and diff < v)

                concordance_matrix[x][y] = av
                non_discordance_matrix[x][y] = (1 if a_are_vetoes_respected else 0)
                
                concordance_matrix[y][x] = bv
                non_discordance_matrix[y][x] = (1 if b_are_vetoes_respected else 0)

        return (concordance_matrix, non_discordance_matrix)

    def __get_outranking_matrix__(self, concordance_matrix, non_discordance_matrix, concordance_threshold):
        size = len(self.names)
        outranking_matrix = [[0] * size for _ in range(size)]

        for x in range(size):
            for y in range(x, size):
                if (x == y):
                    outranking_matrix[x][y] = 'x'
                    continue
                
                ac = concordance_matrix[x][y]
                av = non_discordance_matrix[x][y]
                bc = concordance_matrix[y][x]
                bv = non_discordance_matrix[y][x]
                outranking_matrix[x][y] = (ac > concordance_threshold) and (av)
                outranking_matrix[y][x] = (bc > concordance_threshold) and (bv)

        return outranking_matrix

    def __get_kernels__(self, result_matrix):
        size = len(self.names)
        kernels = []
        for col in range(size):
            # print('> Processing candidate \'{}\'...'.format(self.names[col]))
            is_kernel = True
            for row in range(size):
                if ((result_matrix[row][col] != 'x') and (result_matrix[row][col])):
                    # print('> Outranking found at [{}, {}]!'.format(row, col))
                    is_kernel = False
                    break

            if (is_kernel):
                kernels.append(self.names[col])
        return kernels

    # Solve the problem
    def solve(
        self,
        weights : Union[str, list],
        prefs : Union[str, List[str]],
        vetoes : List, 
        concordance_threshold : List, 
        preference_thresholds : List,
        weights_idx : int = 0,
    ) -> Dict:

        # Define the weights of the attributes
        if type(weights) == str:
            self.weights = self.get_weights(weights)[weights_idx]
        elif type(weights) == list:
            self.weights = weights

        # Check if the lengths matches togethers
        assert len(self.weights) == self.constraints_length, '\033[91m' + "The number of weights as a variable length, please give a consistent length with the matrix constraints !" + '\033[0m'

        # Check variable types
        assert all(isinstance(e, (int, float)) for e in self.weights), '\033[91m' + "The weights as variable types, please give only integers and float !" + '\033[0m'

        # Get preferences
        if type(prefs) == str:
            self.preferences = self.get_preferences(prefs)
        elif type(prefs) == list:
            self.preferences = prefs

        # Check if has preferences other than max and min 
        assert all([a in ['max', 'min'] for a in sorted(list(set(self.preferences)))]), '\033[91m' + "The preferences need to containt only min and max. Found : " + str(sorted(list(set(self.preferences)))) + '\033[0m'
        
        # Check if the lengths matches togethers
        assert len(self.preferences) == self.constraints_length, '\033[91m' + "The preferences data as a variable length, please give a consistent length with the matrix constraints !" + '\033[0m'
        assert len(vetoes) == self.constraints_length, '\033[91m' + "The vetoes data as a variable length, please give a consistent length with the matrix constraints !" + '\033[0m'
        if (preference_thresholds != None):
            assert len(preference_thresholds) == self.constraints_length, '\033[91m' + "The preference thresholds data as a variable length, please give a consistent length with the matrix constraints !" + '\033[0m'

        # Compute the matrices
        (concordance_matrix, non_discordance_matrix) = \
            self.__get_electre1_matrices__(weights, prefs, vetoes, preference_thresholds)

        # Compute outranking matrix from concordance and non-discordance
        outranking_matrix = self.__get_outranking_matrix__(
            concordance_matrix, non_discordance_matrix, concordance_threshold)

        # Compute the graph kernels
        kernels = self.__get_kernels__(outranking_matrix)

        # Perform robustness analysis
        robustness_analysis_results, frequent_kernels = \
            self.__robustness_analysis__(concordance_matrix, non_discordance_matrix)

        # Display the matrices
        if (self.verbose):
            self.__print_electre__(
                concordance_matrix, 
                non_discordance_matrix, 
                outranking_matrix, 
                kernels,
                robustness_analysis_results,
                frequent_kernels,
            )

        return {
            "kernels": kernels,
            "frequent_kernels": frequent_kernels
        }