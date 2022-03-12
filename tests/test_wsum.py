from operator import index
import unittest
from EasyMCDM.models.WSum import WSum

class TestWSumMethods(unittest.TestCase):

    def test_global_wsum(self):

        d = "data/donnees.csv"

        p = WSum(data=d, verbose=True)
        # 3 dimensional Pareto on :   Price   Max Speed t-1000 meters 
        res = p.solve(pref_indexes=[0,1,6],prefs=["min","max","min"], weights=[0.001,2,3], target='min')

        self.assertEqual(
            'bmw_320d',
            res[0][1]
        )

        self.assertEqual(
            'cit_xsara',
            res[9][1]
        )

        res = p.solve(pref_indexes=[1],prefs=["max"], weights=[1], target='max')

        self.assertEqual(
            'bmw_320d',
            res[0][1]
        )

        self.assertEqual(
            'cit_xsara',
            res[9][1]
        )

        res = p.solve(pref_indexes=[0,1],prefs=["min","max"], weights=[1,1], target='max')

        self.assertEqual(
            'cit_xsara',
            res[0][1]
        )

        self.assertEqual(
            'bmw_320d',
            res[8][1]
        )

        self.assertEqual(
            'rnlt_safrane',
            res[9][1]
        )


if __name__ == '__main__':
    unittest.main()