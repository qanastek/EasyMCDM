import numpy as np
from typing import Dict, List, Tuple, Union
from EasyMCDM.models.MCDM import MCDM

class WSum(MCDM):
    
    # Constructor
    def __init__(self, data : Union[str, np.ndarray, dict], col_sep=',', row_sep='\n', verbose=True):
        super().__init__(data, col_sep=col_sep, row_sep=row_sep, verbose=verbose)

    # Solve the problem by returning a ranking in 0(n)
    def solve(self, pref_indexes: List[int], prefs: List[str], weights: List[float], target='min') -> Dict:
        keys=[key for key in self.matrix.keys() ]
        assert len(pref_indexes) == len(weights)," - WSum.solve() - weights size doesn't match threshold_indexes size"
        assert len(pref_indexes) == len(prefs)," - WSum.solve() - prefs size doesn't match pref_indexes size"

        weights = [ weights[i] if prefs[i] == target else weights[i]*-1 for i in range(len(weights)) ]
        matrix = np.asarray([np.array(val) for val in self.matrix.values()])
        matrix = matrix[:, pref_indexes]

        res = []
        for i in range(len(matrix)):
            mul = np.multiply(matrix[i], weights)
            res.append(np.sum(mul))
        argres = np.asarray(res).argsort() if target=='min' else (-np.asarray(res)).argsort()

        res = [ res[index] for index in argres ]
        ranks = [ i for i in range(1,len(argres)+1)]
        labels = [ keys[index] for index in argres]
        scores = [ (rank, key, score) for key, score, rank in zip( labels, res, ranks ) ]
        return scores