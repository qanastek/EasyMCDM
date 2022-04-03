from typing import Dict, List, Tuple, Union

from EasyMCDM.models.MCDM import MCDM

import numpy as np


class WeightedSum(MCDM):
    
    # Constructor
    def __init__(self, data : Union[str, np.ndarray, dict], col_sep=',', row_sep='\n', verbose=True, standardize=False, normalize=True):
        super().__init__(data, col_sep=col_sep, row_sep=row_sep, verbose=verbose, standardize=standardize, normalize=normalize)
        self.scaled = standardize or normalize 

    # Solve the problem by returning a ranked list of tuple in 0(n) iterations
    def solve(self, pref_indexes: List[int], prefs: List[str], weights: List[float], target='min') -> List[tuple]:

        assert len(pref_indexes) == len(weights)," - WeightedSum.solve() - weights size doesn't match the pref_indexes size"
        assert len(pref_indexes) == len(prefs)," - WeightedSum.solve() - prefs size doesn't match pref_indexes size"

        # Adjusting weights
        weights = [weights[i] if prefs[i] == target else weights[i]*-1 for i in range(len(weights))]

        # Get only preferred index columns in data
        if ( self.scaled ):
            matrix = np.asarray([np.array(val)[pref_indexes] for val in self.scaled_matrix])
        else:
            matrix = np.asarray([np.array(val)[pref_indexes] for val in self.matrix.values()])

        # Weighted Summing
        res = [np.sum(line) for line in np.multiply(matrix[:], [weights for i in self.matrix])]

        # Shift Index sort on weighted sum 
        argres = np.asarray(res).argsort() if target=='max' else (-np.asarray(res)).argsort()

        # Sorting results
        res = [res[index] for index in argres]

        if ( target == 'max'):
            ranks = [len(argres)+1-i for i in range(1,len(argres)+1)]
        else:
            ranks = [i for i in range(1,len(argres)+1)]

        keys = list(self.matrix.keys())
        labels = [keys[index] for index in argres]
        scores = [(rank, key, score) for key, score, rank in zip(labels, res, ranks)]

        if "max" in target:
            scores.reverse()

        return scores