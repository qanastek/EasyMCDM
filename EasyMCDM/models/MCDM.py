from numpy import ndarray
from typing import Dict, List, Tuple, Union

class MCDM(object):

    # Memory allocation
    __slots__ = ['verbose', 'matrix', 'names', 'weights', 'preferences', 'promethee_matrix', 'constraints_length', 'col_sep', 'row_sep']

    # Constructor
    def __init__(self, data : Union[str, ndarray, dict], col_sep=',', row_sep='\n', verbose=True):

        # Line & column separator
        self.col_sep, self.row_sep = col_sep, row_sep

        # Verbose ?
        self.verbose = verbose

        FAIL = '\033[91m'
        ENDC = '\033[0m'

        # Init
        self.names = []
        self.matrix = {}
        self.weights = []
        self.preferences = []

        # Load the data matrix
        if type(data) == str:
            self.matrix = self.load_data(data)
        elif type(data) == ndarray:
            self.matrix = {d[0] : [float(i) for i in d[1:]] for d in data}
        elif type(data) == dict:
            self.matrix = data

        # Check matrix types
        assert self.check_consistency_dict(self.matrix) == True, MCDM.FAIL + "The input data as a variable length, please give a consistent length !" + MCDM.ENDC

        # Get subjects names
        self.names = list(self.matrix.keys())

        # Number of constraints
        self.constraints_length = len(list(self.matrix.values())[0])

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
        f = open(path,"r")
        for line in [d.split(self.col_sep) for d in f.read().split(self.row_sep) if len(d) > 0]:
            matrix[str(line[0])] = [float(a) for a in line[1:]]
        f.close()
        return matrix
    
    # Read the line of preferences
    def get_preferences(self, path):
        
        f = open(path,"r")
        content = f.read().replace(self.row_sep,"")
        f.close()

        # Check if file is empty
        assert len(content) > 0, MCDM.FAIL + "Preferences file is empty!" + MCDM.ENDC

        return content.split(",")

    # Read the lines of weights
    def get_weights(self, path) -> List:
        f = open(path,"r")
        content = f.read()
        f.close()
        return [[float(i) for i in w.split(self.col_sep)] for w in content.split(self.row_sep) if len(w) > 0]
