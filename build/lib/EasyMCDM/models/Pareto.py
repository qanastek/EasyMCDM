from numpy import ndarray
from typing import Dict, List, Tuple, Union

from EasyMCDM.models.MCDM import MCDM

class Pareto(MCDM):
    
    # Constructor
    def __init__(self, data : Union[str, ndarray, dict], verbose=True):
        super().__init__(data,verbose)
        self.nbr_items = {}

    # Solve the problem
    def solve(self, indexes: List[str], prefs: List[str]) -> Dict:

        # Number of elements
        self.nbr_items = len(prefs)

        assert len(indexes) == self.nbr_items, MCDM.FAIL + "Indexes and preferences length aren't the sames!" + MCDM.ENDC

        # Initialize
        dominance = {c : {"Dominated_By":[], "Very_Dominated_By":[]} for c in self.matrix}

        # For each cars
        for c1 in self.matrix:
            for c2 in self.matrix:

                # Prevent diagonal
                if c1 == c2 :
                    continue

                nbCritDominated, nbCritEquals = 0, 0

                # For each item check if dominate or dominated
                for i in range(self.nbr_items):

                    # Get index and preference
                    idx, pref = indexes[i], prefs[i]

                    # Get values
                    c1_value, c2_value = self.matrix[c1][idx], self.matrix[c2][idx]

                    # Check if dominated or not
                    if c1_value == c2_value:
                        nbCritEquals +=1
                    elif (pref == 'min'and c1_value < c2_value) or (pref == 'max' and c1_value > c2_value):
                        nbCritDominated +=1

                # If very dominated
                if nbCritDominated == self.nbr_items:
                    dominance[c2]['Very_Dominated_By'].append(c1)
                
                # If dominated
                if nbCritDominated + nbCritEquals == self.nbr_items:
                    dominance[c2]['Dominated_By'].append(c1)

        return dominance