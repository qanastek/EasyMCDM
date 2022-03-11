from typing import Dict, List, Union

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
        non_discondance_matrix, 
        result_matrix, 
        kernels,
    ):
        print()
        for x in range(len(concordance_matrix)):
            print('\t'.join(["{:1.3f}".format(y) if y != 'x' else y for y in concordance_matrix[x]]))

        print()
        for x in range(len(non_discondance_matrix)):
            print('\t'.join(["{:1.3f}".format(y) if y != 'x' else y for y in non_discondance_matrix[x]]))

        print()
        for x in range(len(result_matrix)):
            print('\t'.join([str(y) for y in result_matrix[x]]))

        print()
        print(kernels)
        
        return

    def __get_electre1_matrices__(self, weights, preferences, vetoes, indifference_threshold, preference_thresholds):
        size = self.constraints_length

        concordance_matrix = [[0] * size for _ in range(size)]
        non_discondance_matrix = [[0] * size for _ in range(size)]
        result_matrix = [[0] * size for _ in range(size)]

        # TODO: 
        data = list(self.matrix.values())

        for x in range(size):
            for y in range(x, size):
                if (x == y):
                    concordance_matrix[x][y] = non_discondance_matrix[x][y] = result_matrix[x][y] = 'x'
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
                    points = 0.0

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
                non_discondance_matrix[x][y] = (1 if a_are_vetoes_respected else 0)
                result_matrix[x][y] = (av > indifference_threshold) and (a_are_vetoes_respected)
                
                concordance_matrix[y][x] = bv
                non_discondance_matrix[y][x] = (1 if b_are_vetoes_respected else 0)
                result_matrix[y][x] = (bv > indifference_threshold) and (b_are_vetoes_respected)

        return (concordance_matrix, non_discondance_matrix, result_matrix)

    def __get_kernels__(self, result_matrix):
        kernels = []
        for y in range(self.constraints_length):
            is_kernel = True
            for x in range(self.constraints_length):
                if ((result_matrix[x][y] != 'x') and (result_matrix[x][y])):
                    is_kernel = False
                    break

            if (is_kernel):
                kernels.append(self.names[y])
        return kernels

    # Solve the problem
    def solve(
        self,
        weights : Union[str, list],
        prefs : Union[str, List[str]],
        vetoes : List, 
        indifference_threshold : List, 
        preference_thresholds : List,
        weights_idx : int = 0,
    ) -> Dict:

        # Define the weights of the attributes
        if type(weights) == str:
            self.weights = self.get_weights(weights)[weights_idx]
        elif type(weights) == list:
            self.weights = weights
        
        # Check if the lengths matches togethers
        assert len(self.weights) == self.constraints_length, MCDM.FAIL + "The number of weights as a variable length, please give a consistent length with the matrix constraints !" + MCDM.ENDC

        # Check variable types
        assert all(isinstance(e, (int, float)) for e in self.weights), MCDM.FAIL + "The weights as variable types, please give only integers and float !" + MCDM.ENDC

        # Get preferences
        if type(prefs) == str:
            self.preferences = self.get_preferences(prefs)
        elif type(prefs) == list:
            self.preferences = prefs

        # Check if has preferences other than max and min 
        assert sorted(list(set(self.preferences))) == ['max', 'min'], MCDM.FAIL + "The preferences need to containt only min and max. Found : " + str(sorted(list(set(self.preferences)))) + MCDM.ENDC
        
        # Check if the lengths matches togethers
        assert len(self.preferences) == self.constraints_length, MCDM.FAIL + "The preferences data as a variable length, please give a consistent length with the matrix constraints !" + MCDM.ENDC
        assert len(vetoes) == self.constraints_length, MCDM.FAIL + "The vetoes data as a variable length, please give a consistent length with the matrix constraints !" + MCDM.ENDC
        if (preference_thresholds != None):
            assert len(preference_thresholds) == self.constraints_length, MCDM.FAIL + "The preference thresholds data as a variable length, please give a consistent length with the matrix constraints !" + MCDM.ENDC

        # Compute the matrices
        (concordance_matrix, non_discondance_matrix, result_matrix) = \
            self.__get_electre1_matrices__(weights, prefs, vetoes, indifference_threshold, preference_thresholds)

        # Compute the graph kernels
        kernels = self.__get_kernels__(result_matrix)

        # Display the matrices
        if (self.verbose):
            self.__print_electre__(
                concordance_matrix, 
                non_discondance_matrix, 
                result_matrix, 
                kernels,
            )

        return {
            "kernels": kernels,
        }