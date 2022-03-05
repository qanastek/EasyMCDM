import numpy as np
from prettytable import PrettyTable
from typing import Dict, List, Tuple, Union

FAIL = '\033[91m'
ENDC = '\033[0m'

class Promethee(object):

    __slots__ = ['verbose', 'matrix', 'names', 'weights', 'preferences', 'promethee_matrix']

    # Constructor
    def __init__(self, verbose=True):

        # Verbose or not
        self.verbose = verbose

        # Others
        self.names = []
        self.matrix = {}
        self.weights = []
        self.preferences = []
        self.promethee_matrix = {}

    # Check data length consistency
    def check_consistency_dict(self, m):

        previous_lenght = -1

        for s in m:

            current = len(m[s])

            if previous_lenght == -1:
                previous_lenght = current
            elif previous_lenght != current:
                return False

        return True

    # Load the csv as a hashmap
    def load_data(self, path):
        matrix = {}
        for line in [d.split(",") for d in open(path,"r").read().split("\n") if len(d) > 0]:
            matrix[str(line[0])] = [float(a) for a in line[1:]]
        return matrix

    # Find the best value between both items of the pair
    def best(self, a, b, w, s) -> Tuple:

        if (s == "min" and a < b) or (s == "max" and a > b):
            return (w, 0.0)
        else:
            return (0.0, w)

    # Read the lines of weights
    def get_weights(self, path) -> List:
        return [[float(i) for i in w.split(",")] for w in open(path,"r").read().split("\n") if len(w) > 0]

    # Read the line of preferences
    def get_preferences(self, path):
        content = open(path,"r").read().replace("\n","")
        if len(content) <= 0:
            print("Preferences file is empty!")
            exit(0)
        return content.split(",")

    # Compute
    def compute(self, a1, a2, weights, preferences) -> Tuple[float, float]:

        res_1, res_2 = [], []

        # Pour chaque champs
        for v1, v2, w, s in zip(a1, a2, weights, preferences):
            r1, r2 = self.best(v1,v2,w,s)
            res_1.append(r1)
            res_2.append(r2)

        return (sum(res_1), sum(res_2))

    # Compute the Promethee matrix
    def get_promethee_matrix(self, names, weights, preferences) -> Dict:

        # Instantiate empty matrix
        res = {}

        # For each subject compute the promethee value
        for i in names:

            for j in names:

                # Jump diagonal
                if i == j:
                    res[(i,j)] = 0.0
                    continue

                # Compute the promethee value
                r1, r2 = self.compute(self.matrix[i], self.matrix[j], weights, preferences)
                res[(i,j)] = r1
                res[(j,i)] = r2
        
        # Return Promethee matrix
        return res

    # Compute the Phi values
    def get_phi(self, names, promethee_matrix) -> Tuple[Tuple, Tuple, List]:

        # Instantiate empty hashmap
        phi_positive = {a: 0.0 for a in names}
        phi_negative = {a: 0.0 for a in names}

        # Phi Positive
        for i, j in promethee_matrix.keys():
            phi_positive[i] += promethee_matrix[(i,j)]

        # Phi Negative
        for i in names:
            for j in names:
                phi_negative[j] += promethee_matrix[(i,j)]

        # Phi Neutral
        phi = [p-n for p, n in zip(phi_positive.values(), phi_negative.values())]

        return phi_positive, phi_negative, phi

    # Build the matrix to display
    def get_printable_matrix(self, names, promethee_matrix, phi_positive, phi_negative, phi) -> str:
        x = PrettyTable()
        x.field_names = [""] + names + ["ϕ+","ϕ"]
        for idx, i in enumerate(names):
            local = []
            local.append(i)
            for j in names:
                local.append('%.2f' % promethee_matrix[(i,j)])
            local.append('%.2f' % phi_positive[i])
            local.append('%.2f' % phi[idx])
            x.add_row(local)
        x.add_row(["ϕ-"] + ['%.2f' % a for a in list(phi_negative.values())] + ["",""])
        return str(x)

    # Sort phi and subjects to get the ranking
    def sort_res(self, names, phi_values, reverse=False) -> List:

        # Create tuples for each subject and phi value
        tuples = [(a, b) for a, b in zip(names, phi_values)]

        # Order this list of tuple by phi
        ordored_tuples = sorted(tuples, key=lambda tup: tup[1], reverse=reverse)

        return ordored_tuples

    # Get and print sorted tuples
    def display_sorted(self, title, names, phi_values, reverse=False) -> List:

        # Get sorted tuples
        ordored_tuples = self.sort_res(names, phi_values, reverse=reverse)
        
        if self.verbose:
            print("\n\n" + title)
            print("*"*len(title))
            print("\n".join(["#" + str(i+1) + " " + a + " \t: " + '%.2f' % b for i,(a,b) in enumerate(ordored_tuples)]))

        return ordored_tuples

    # Solve the problem
    def solve(
        self,
        data : Union[str, np.ndarray, dict],
        weights : Union[str, list],
        prefs : Union[str, List[str]],
        weights_idx=0
    ) -> Dict:

        # Load the data matrix
        if type(data) == str:
            self.matrix = self.load_data(data)
        elif type(data) == np.ndarray:
            self.matrix = {d[0] : [float(i) for i in d[1:]] for d in data}
        elif type(data) == dict:
            self.matrix = data

        # Check matrix types
        assert self.check_consistency_dict(self.matrix) == True, FAIL + "The input data as a variable length, please give a consistent length !" + ENDC

        # Get subjects names
        self.names = list(self.matrix.keys())

        # Number of constraints
        constraints_length = len(list(self.matrix.values())[0])

        # Define the weights of the attributes
        if type(weights) == str:
            self.weights = self.get_weights(weights)[weights_idx]
        elif type(weights) == list:
            self.weights = weights
        
        # Check if the lengths matches togethers
        assert len(self.weights) == constraints_length,  FAIL + "The number of weights as a variable length, please give a consistent length with the matrix constraints !" + ENDC

        # Check variable types
        assert all(isinstance(e, (int, float)) for e in self.weights), FAIL + "The weights as variable types, please give only integers and float !" + ENDC

        # Get preferences
        if type(prefs) == str:
            self.preferences = self.get_preferences(prefs)
        elif type(prefs) == list:
            self.preferences = prefs

        # Check if has preferences other than max and min 
        assert sorted(list(set(self.preferences))) == ['max', 'min'], FAIL + "The preferences need to containt only min and max. Found : " + str(sorted(list(set(self.preferences)))) + ENDC
        
        # Check if the lengths matches togethers
        assert len(self.preferences) == constraints_length, FAIL + "The preferences data as a variable length, please give a consistent length with the matrix constraints !" + ENDC

        # Compute the promethee matrix
        self.promethee_matrix = self.get_promethee_matrix(self.names, self.weights, self.preferences)

        # Compute all three phi values
        phi_positive, phi_negative, phi = self.get_phi(self.names, self.promethee_matrix)

        # Display the matrix
        res_matrix = self.get_printable_matrix(self.names, self.promethee_matrix, phi_positive, phi_negative, phi)

        if self.verbose:
            print("Weights : ", self.weights)
            print("Preferences : ", self.preferences)
            print(res_matrix)

        # Get phi values
        phi_neg = self.display_sorted("Ranking ϕ- :", self.names, list(phi_negative.values()))
        phi_pos = self.display_sorted("Ranking ϕ+ :", self.names, list(phi_positive.values()), reverse=True)
        phi = self.display_sorted("Ranking ϕ :", self.names, phi, reverse=True)

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
