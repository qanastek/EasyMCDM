from EasyMCDM.models.Electre import Electre
from EasyMCDM.models.Promethee import Promethee
from EasyMCDM.models.Pareto import Pareto
from EasyMCDM.models.WeightedSum import WeightedSum
from EasyMCDM.models.Irmo import Irmo


##############################################################################
# [ENTRYPOINTS]
##############################################################################
if __name__ == "__main__":
    data = {
        "alfa_156":     [23817.0, 201.0, 8.0, 39.6, 6.0, 378.0, 31.2], 
        "audi_a4":      [25771.0, 195.0, 5.7, 35.8, 7.0, 440.0, 33.0], 
        "cit_xantia":   [25496.0, 195.0, 7.9, 37.0, 2.0, 480.0, 34.0], 
        "peugeot_406":  [25649.0, 191.0, 8.3, 34.4, 2.0, 430.0, 34.6], 
        "saab_tid":     [26183.0, 199.0, 7.8, 35.7, 5.0, 494.0, 32.0], 
        "rnlt_laguna":  [23664.0, 194.0, 7.7, 37.4, 4.0, 452.0, 33.8], 
        "vw_passat":    [23344.0, 195.0, 7.6, 34.4, 3.0, 475.0, 33.6], 
        "bmw_320d":     [26260.0, 209.0, 6.6, 36.6, 4.0, 440.0, 30.9], 
        "cit_xsara":    [19084.0, 182.0, 6.4, 40.6, 8.0, 408.0, 33.5], 
        "rnlt_safrane": [29160.0, 203.0, 7.5, 34.5, 1.0, 520.0, 32.0]
    }
    criteria_idx =          [    1,     3,     6 ]
    criteria_prefs =        ["min", "min", "min"]
    criteria_weights =      [ 15,    1,  5, ]
    weights =               [ 0,  0.7,  0,  0.1,  0,  0,  0.2]
    prefs =                 [ "min", "max", "min", "min", "min", "max", "min"]
    vetoes =                [ 0,  3.50,  0,  1.50,  0, 0,  1]
    preference_thresholds = [ 100000,  195,  10000,  40,  0, 0, 33  ]
    indifference_threshold = 0.55

    verbose = True
    w = WeightedSum(data=data, verbose=verbose)
    pa = Pareto(data=data, verbose=verbose)
    pr = Promethee(data=data, verbose=verbose)
    e = Electre(data=data, verbose=verbose)

    re = e.solve(weights, prefs, vetoes, indifference_threshold, preference_thresholds)
    rpr = pr.solve(weights=weights, prefs=prefs)
    rpa = pa.solve(indexes=criteria_idx, prefs=criteria_prefs)
    rw = w.solve(pref_indexes=criteria_idx, prefs=criteria_prefs, weights=criteria_weights, target='min')

    print(re)
    print(rpr)
    print(rpa)
    print(rw)