import unittest
from EasyMCDM.models.Irmo import Irmo

class TestIrmoMethods(unittest.TestCase):

    def test_str_str_str(self):

        p = Irmo(data="data/donnees.csv", verbose=False)
        res = p.solve(
            indexes=[0,1,4,5], # price -> max_speed -> comfort -> trunk_space
            prefs=["min","max","min","max"]
        )
        
        self.assertEqual(
            "saab_tid",
            res["best"]
        )

if __name__ == '__main__':
    unittest.main()