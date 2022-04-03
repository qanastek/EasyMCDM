from operator import index
import unittest
import pandas as pd
from EasyMCDM.models.Pareto import Pareto
from EasyMCDM.models.Promethee import Promethee

class TestParetoMethods(unittest.TestCase):

    def test_audi_pareto(self):

        d = "data/donnees.csv"

        p = Pareto(data=d, verbose=True)
        # 3 dimensional Pareto on :   Price   Max Speed t-1000 meters 
        res = p.solve(indexes=[0,1,6], prefs=["min","max","min"])

        # Audi A4 dominated by alfa 156
        self.assertEqual(
            ['alfa_156'],
            res['audi_a4']['Strongly-Dominated-by']
        )

        self.assertEqual(
            ['alfa_156'],
            res['audi_a4']['Dominated-by']
        )

if __name__ == '__main__':
    unittest.main()