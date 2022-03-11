from prettytable import PrettyTable
from typing import Dict, List, Tuple, Union

from EasyMCDM.models.MCDM import MCDM

class Promethee(MCDM):

    # Memory allocation
    __slots__ = ['verbose', 'matrix', 'names', 'weights', 'preferences', 'promethee_matrix']

    # Constructor
    def __init__(self, data : Union[str, dict], col_sep=',', row_sep='\n', verbose=True):
        super().__init__(data, col_sep=col_sep, row_sep=row_sep, verbose=verbose)
        self.promethee_matrix = {}

    # Find the best value between both items of the pair
    def __best(self, a, b, w, s) -> Tuple:

        if a == b:
            return (0.0, 0.0)

        elif (s == "min" and a < b) or (s == "max" and a > b):
            return (w, 0.0)

        return (0.0, w)

    # Compute
    def __compute(self, a1, a2) -> Tuple[float, float]:

        res_1, res_2 = [], []

        # Pour chaque champs
        for v1, v2, w, s in zip(a1, a2, self.weights, self.preferences):
            r1, r2 = self.__best(v1,v2,w,s)
            res_1.append(r1)
            res_2.append(r2)

        return (sum(res_1), sum(res_2))

    # Compute the Promethee matrix
    def __get_promethee_matrix(self) -> Dict:

        # Instantiate empty matrix
        res = {}

        # For each subject compute the promethee value
        for i in self.names:

            for j in self.names:

                # Jump diagonal
                if i == j:
                    res[(i,j)] = 0.0
                    continue

                # Compute the promethee value
                res[(i,j)], res[(j,i)] = self.__compute(self.matrix[i], self.matrix[j])
        
        # Return Promethee matrix
        return res

    # Compute the Phi values
    def __get_phi(self) -> Tuple[Tuple, Tuple, List]:

        # Instantiate empty hashmap
        phi_positive = {a: 0.0 for a in self.names}
        phi_negative = {a: 0.0 for a in self.names}

        # Phi Positive
        for i, j in self.promethee_matrix.keys():
            phi_positive[i] += self.promethee_matrix[(i,j)]

        # Phi Negative
        for i in self.names:
            for j in self.names:
                phi_negative[j] += self.promethee_matrix[(i,j)]

        # Phi Neutral
        phi = [p-n for p, n in zip(phi_positive.values(), phi_negative.values())]

        return phi_positive, phi_negative, phi

    # Build the matrix to display
    def __get_printable_matrix(self, phi_positive, phi_negative, phi) -> str:
        x = PrettyTable()
        x.field_names = [""] + self.names + ["ϕ+","ϕ"]
        for idx, i in enumerate(self.names):
            local = []
            local.append(i)
            for j in self.names:
                local.append('%.2f' % self.promethee_matrix[(i,j)])
            local.append('%.2f' % phi_positive[i])
            local.append('%.2f' % phi[idx])
            x.add_row(local)
        x.add_row(["ϕ-"] + ['%.2f' % a for a in list(phi_negative.values())] + ["",""])
        return str(x)

    # Sort phi and subjects to get the ranking
    def __sort_res(self, names, phi_values, reverse=False) -> List:

        # Create and order tuples for each subject and phi value
        return sorted(
            [(a, b) for a, b in zip(names, phi_values)],
            key=lambda tup: tup[1],
            reverse=reverse
        )

    # Get and print sorted tuples
    def __display_sorted(self, title, names, phi_values, reverse=False) -> List:

        # Get sorted tuples
        ordored_tuples = self.__sort_res(names, phi_values, reverse=reverse)
        
        if self.verbose:
            print("\n\n" + title)
            print("*"*len(title))
            print("\n".join(["#" + str(i+1) + " " + a + " \t: " + '%.2f' % b for i,(a,b) in enumerate(ordored_tuples)]))

        return ordored_tuples

    # Solve the problem
    def solve(
        self,
        weights : Union[str, list],
        prefs : Union[str, List[str]],
        weights_idx = 0
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

        # Compute the promethee matrix
        self.promethee_matrix = self.__get_promethee_matrix()

        # Compute all three phi values
        phi_positive, phi_negative, phi = self.__get_phi()

        # Display the matrix
        if self.verbose:
            res_matrix = self.__get_printable_matrix(phi_positive, phi_negative, phi)
        else:
            res_matrix = "Please run verbose to get the Promethee II matrix!"

        if self.verbose:
            print("Weights : ", self.weights)
            print("Preferences : ", self.preferences)
            print(res_matrix)

        # Get phi values
        phi_neg = self.__display_sorted("Ranking ϕ- :", self.names, list(phi_negative.values()))
        phi_pos = self.__display_sorted("Ranking ϕ+ :", self.names, list(phi_positive.values()), reverse=True)
        phi = self.__display_sorted("Ranking ϕ :", self.names, phi, reverse=True)

        if self.verbose:
            print("\n\nBest ϕ- is ", phi_neg[0][0], " with ", '%.2f' % phi_neg[0][1])
            print("Best ϕ+ is ", phi_pos[0][0], " with ", '%.2f' % phi_pos[0][1])
            print("Best ϕ  is ", phi[0][0], " with ", '%.2f' % phi[0][1])
        
        return {
            "phi_negative": phi_neg,
            "phi_positive": phi_pos,
            "phi": phi,
            "matrix": res_matrix,
        }