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
            res['audi_a4']['Very_Dominated_By']
        )

        self.assertEqual(
            ['alfa_156'],
            res['audi_a4']['Dominated_By']
        )

class TestPrometheeMethods(unittest.TestCase):

    def test_str_str_str(self):

        d = "data/donnees.csv"
        w = "data/weights.txt"
        prefs = "data/preferences.txt"

        p = Promethee(data=d, verbose=True)
        res = p.solve(weights=w, prefs=prefs)

        # Test Phi Negative
        self.assertEqual(
            ('rnlt_safrane', 2.5200000000000005),
            res["phi_negative"][0]
        )

        # Test Phi Positive
        self.assertEqual(
            ('rnlt_safrane', 6.300000000000001),
            res["phi_positive"][0]
        )
        
        # Test Phi Neutral
        self.assertEqual(
            ('rnlt_safrane', 3.7800000000000002),
            res["phi"][0]
        )

        # Matrix
        self.assertEqual(
            open("outputs/matrix.txt","r").read(),
            res["matrix"]
        )

    def test_numpy_list_list(self):

        d = pd.read_csv('data/donnees.csv', header=None).to_numpy()
        w = [0.14,0.14,0.14,0.14,0.14,0.14,0.14]
        prefs = ["min","max","min","min","min","max","min"]

        p = Promethee(data=d, verbose=True)
        res = p.solve(weights=w, prefs=prefs)

        # Test Phi Negative
        self.assertEqual(
            ('rnlt_safrane', 2.5200000000000005),
            res["phi_negative"][0]
        )

        # Test Phi Positive
        self.assertEqual(
            ('rnlt_safrane', 6.300000000000001),
            res["phi_positive"][0]
        )
        
        # Test Phi Neutral
        self.assertEqual(
            ('rnlt_safrane', 3.7800000000000002),
            res["phi"][0]
        )

        # Matrix
        self.assertEqual(
            open("outputs/matrix.txt","r").read(),
            res["matrix"]
        )

    def test_dict_list_list(self):

        d = { "alfa_156": [23817.0, 201.0, 8.0, 39.6, 6.0, 378.0, 31.2], "audi_a4": [25771.0, 195.0, 5.7, 35.8, 7.0, 440.0, 33.0], "cit_xantia": [25496.0, 195.0, 7.9, 37.0, 2.0, 480.0, 34.0], "peugeot_406": [25649.0, 191.0, 8.3, 34.4, 2.0, 430.0, 34.6], "saab_tid": [26183.0, 199.0, 7.8, 35.7, 5.0, 494.0, 32.0], "rnlt_laguna": [23664.0, 194.0, 7.7, 37.4, 4.0, 452.0, 33.8], "vw_passat": [23344.0, 195.0, 7.6, 34.4, 3.0, 475.0, 33.6], "bmw_320d": [26260.0, 209.0, 6.6, 36.6, 4.0, 440.0, 30.9], "cit_xsara": [19084.0, 182.0, 6.4, 40.6, 8.0, 408.0, 33.5], "rnlt_safrane": [29160.0, 203.0, 7.5, 34.5, 1.0, 520.0, 32.0] }
        w = [0.14,0.14,0.14,0.14,0.14,0.14,0.14]
        prefs = ["min","max","min","min","min","max","min"]

        p = Promethee(data=d, verbose=True)
        res = p.solve(weights=w, prefs=prefs)

        # Test Phi Negative
        self.assertEqual(
            ('rnlt_safrane', 2.5200000000000005),
            res["phi_negative"][0]
        )

        # Test Phi Positive
        self.assertEqual(
            ('rnlt_safrane', 6.300000000000001),
            res["phi_positive"][0]
        )
        
        # Test Phi Neutral
        self.assertEqual(
            ('rnlt_safrane', 3.7800000000000002),
            res["phi"][0]
        )

        # Matrix
        self.assertEqual(
            open("outputs/matrix.txt","r").read(),
            res["matrix"]
        )

if __name__ == '__main__':
    unittest.main()