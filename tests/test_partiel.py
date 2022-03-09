from operator import index
import unittest
import pandas as pd
from EasyMCDM.models.Promethee import Promethee

class TestPrometheeMethods(unittest.TestCase):

    def test_str_str_str(self):

        d = "data/partiels_donnees.csv"

        p = Promethee(data=d, verbose=False)
        res = p.solve(
            weights=[0.3, 0.2, 0.2, 0.1, 0.2],
            prefs=["min","min","max","max","max"]
        )

        assert res["phi_negative"] == [('A', 0.8), ('C', 1.4000000000000001), ('D', 1.7), ('E', 2.4), ('B', 3.0999999999999996)], "Phi Negative are differents!"
        assert res["phi_positive"] == [('A', 3.0), ('C', 2.2), ('D', 1.9), ('E', 1.4000000000000001), ('B', 0.9)], "Phi positive are differents!"
        assert res["phi"] == [('A', 2.2), ('C', 0.8), ('D', 0.19999999999999996), ('E', -0.9999999999999998), ('B', -2.1999999999999997)], "Phi are differents!"

if __name__ == '__main__':
    unittest.main()