import unittest
from EasyMCDM.models.Electre import Electre

class TestElectre1v(unittest.TestCase):

    def test_solve_exam(self):
        data = {
            "A1" : [80, 90,  600, 5.4,  8,  5],
            "A2" : [65, 58,  200, 9.7,  1,  1],
            "A3" : [83, 60,  400, 7.2,  4,  7],
            "A4" : [40, 80, 1000, 7.5,  7, 10],
            "A5" : [52, 72,  600, 2.0,  3,  8],
            "A6" : [94, 96,  700, 3.6,  5,  6],
        }
        weights = [0.1, 0.2, 0.2, 0.1, 0.2, 0.2]
        prefs = ["min", "max", "min", "min", "min", "max"]
        vetoes = [45, 29, 550, 6, 4.5, 4.5]
        indifference_threshold = 0.6
        preference_thresholds = None

        e = Electre(data=data, verbose=False)
        
        results = e.solve(weights, prefs, vetoes, indifference_threshold, preference_thresholds)
        self.assertEqual(
            ['A4', 'A5'],
            results['kernels']
        )

        indifference_threshold = 0.79
        results = e.solve(weights, prefs, vetoes, indifference_threshold, preference_thresholds)
        self.assertEqual(
            ['A1', 'A2', 'A4', 'A5'],
            results['kernels']
        )

if __name__ == '__main__':
    unittest.main()