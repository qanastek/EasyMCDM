from typing import Dict, List, Tuple, Union
from itertools import combinations
from EasyMCDM.models.MCDM import MCDM

class Pareto(MCDM):
    
    # Constructor
    def __init__(self, data : Union[str, dict], col_sep=',', row_sep='\n', verbose=True):
        super().__init__(data, col_sep=col_sep, row_sep=row_sep, verbose=verbose)
        self.nbr_items = {}

    # Solve the problem by returning a Pareto Dominance Dict in O( len(pref) * ( len(combination(candidate) ) )
    def solve(self, indexes: List[str], prefs: List[str]) -> Dict:
        self.nbr_items = len(prefs)
        assert len(indexes) == self.nbr_items, MCDM.FAIL + "Indexes and preferences length aren't the sames!" + MCDM.ENDC

        # Result : dominance dictonnary
        self.dominance = {c : {"Weakly-dominated-by":[], "Dominated-by":[]} for c in self.matrix}
        
        # Get all pairs of candidate
        cndt_pairs = combinations(self.matrix,2)

        # Foreach pair of candidate
        for cndt_pair in cndt_pairs:

            cndt1, cndt2 = cndt_pair
            nbCritDominatedCndt1, nbCritDominatedCndt2, nbCritEquals = 0, 0, 0

            # For each item check if dominate or dominated
            for i in range(self.nbr_items):

                # Get column index on which we want to search a prefered optimum (min/max)
                idx, pref = indexes[i], prefs[i]

                # Get candidate values to compare
                cndt1_value, cndt2_value = self.matrix[cndt1][idx], self.matrix[cndt2][idx]

                # Dominance checking
                if cndt1_value == cndt2_value:
                    nbCritEquals +=1

                elif pref == 'min':
                    if cndt1_value < cndt2_value:
                        nbCritDominatedCndt1 +=1
                    else:
                        nbCritDominatedCndt2 +=1

                else: # pref == 'max'
                    if cndt1_value > cndt2_value:
                        nbCritDominatedCndt1 +=1
                    else:
                        nbCritDominatedCndt2 +=1

            # If Candidate 2 dominated
            if nbCritDominatedCndt1 + nbCritEquals == self.nbr_items:
                self.dominance[cndt2]['Weakly-dominated-by'].append(cndt1)

                # If candidate 2 very dominated
                if nbCritDominatedCndt1 == self.nbr_items:
                    self.dominance[cndt2]['Dominated-by'].append(cndt1)

            # If Candidate 1 dominated
            elif nbCritDominatedCndt2 + nbCritEquals == self.nbr_items: 
                self.dominance[cndt1]['Weakly-dominated-by'].append(cndt2)

                # If Candidate 1 very dominated
                if nbCritDominatedCndt2 == self.nbr_items:
                    self.dominance[cndt1]['Dominated-by'].append(cndt2)

        return self.dominance