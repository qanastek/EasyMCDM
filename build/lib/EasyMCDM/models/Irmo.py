import math
from typing import Dict, List, Tuple, Union

from EasyMCDM.models.MCDM import MCDM

# Instant-Runoff Multicriteria Optimization (IRMO)
class Irmo(MCDM):

    # Memory allocation
    __slots__ = ['verbose', 'matrix', 'names', 'indexes', 'preferences', 'matrix']

    # Constructor
    def __init__(self, data : Union[str, dict], col_sep=',', row_sep='\n', verbose=True):
        super().__init__(data, col_sep=col_sep, row_sep=row_sep, verbose=verbose)

    # Read the lines of indexes
    def get_indexes(self, path) -> List:
        f = open(path,"r")
        content = f.read()
        f.close()
        return [[int(i) for i in w.split(self.col_sep)] for w in content.split(self.row_sep) if len(w) > 0]

    def __getVector(self, i, idx, banned, nbr_rounds):

        items_lst = []

        for s in self.matrix.keys():

                # Check if already banned
                if s not in banned:
                    insert_value = self.matrix[s][i]
                else:
                    
                    # Best item value
                    if (idx == nbr_rounds - 1 and self.preferences[idx] == "min") or (idx != nbr_rounds - 1 and self.preferences[idx] == "max"):
                        insert_value = math.inf
                    else:
                        insert_value = -math.inf

                items_lst.append(insert_value)

        return items_lst

    # Compute
    def __compute(self) -> Tuple[float, float]:

        banned = []

        # Check if the number of criteria is higher than the number of subjects else reduce the number of rounds
        nbr_rounds = len(self.indexes) if len(self.indexes) <= len(self.matrix.keys()) else len(self.matrix.keys())
    
        # For each criteria
        for idx, i in enumerate(self.indexes):

            # Values for the subjects left
            items_vec = self.__getVector(i, idx, banned, nbr_rounds)

            # Best item value
            if (idx == nbr_rounds - 1 and self.preferences[idx] == "min") or (idx != nbr_rounds - 1 and self.preferences[idx] == "max"):
                value = min(items_vec)
            else:
                value = max(items_vec)

            # Worst item index
            item_idx = items_vec.index(value)
            item_name = list(self.matrix.keys())[item_idx]

            # Ban Worst item
            banned.append(item_name)

        # Reverse the rank
        banned.reverse()

        return {
            "best": banned[0], # Return best
            "eleminated": banned
        }

    # Solve the problem
    def solve(
        self,
        indexes : Union[str, list],
        prefs : Union[str, List[str]],
        indexes_idx = 0
    ) -> Dict:

        # Define the indexes of the attributes
        if type(indexes) == str:
            self.indexes = self.get_indexes(indexes)[indexes_idx]
        elif type(indexes) == list:
            self.indexes = indexes
        
        # Check if the lengths matches togethers
        assert len(self.indexes) <= self.constraints_length, '\033[91m' + "The number of indexes as a variable length, please give a consistent length with the matrix constraints !" + '\033[0m'

        # Check variable types
        assert all(isinstance(e, (int)) for e in self.indexes), '\033[91m' + "The indexes as variable types, please give only integers !" + '\033[0m'

        # Get preferences
        if type(prefs) == str:
            self.preferences = self.get_preferences(prefs)
        elif type(prefs) == list:
            self.preferences = prefs

        # Check if has preferences other than max and min 
        assert all([a in ['max', 'min'] for a in sorted(list(set(self.preferences)))]), '\033[91m' + "The preferences need to containt only min and max. Found : " + str(sorted(list(set(self.preferences)))) + '\033[0m'
        
        # Check if the lengths matches togethers
        assert len(self.preferences) == len(self.indexes), '\033[91m' + "The number of preferences as a variable length, please give a consistent length with the indexes !" + '\033[0m'
        
        return self.__compute()