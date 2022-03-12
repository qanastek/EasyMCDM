import unittest
from EasyMCDM.models.Irmo import Irmo

class TestIrmoMethods(unittest.TestCase):

    def test_str_str_str(self):

        d = "data/partiels_donnees.csv"

        p = Irmo(data=d, verbose=False)
        res = p.solve(
            indexes=[0,1,2],
            prefs=["min","min","max"]
        )
        
        self.assertEqual(
            ['D', 'E', 'C'],
            res["rank"]
        )

if __name__ == '__main__':
    unittest.main()