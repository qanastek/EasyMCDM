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
    # criteria_idx =          [    4,     2,     0]
    # criteria_prefs =        ["min", "min", "min"]
    # criteria_weights =      [ 0.25,  0.25,  0.5]
    criteria_idx =          [    4,     2,     5]
    criteria_prefs =        ["min", "min", "max"]
    criteria_weights =      [ 0.55,  0.25,  0.20]
    weights =               [   0.10,  0.05,  0.05,  0.15,  0.05,  0.20,  0.40]
    prefs =                 [  "min", "max", "min", "min", "min", "max", "min"]
    preference_thresholds = [1250.00,  3.50,  0.50,  1.50,  1.00, 35.00,  1.00]
    vetoes =                [27500.00,  70.50,  10.80,  20.25,  10.50, 65.00,  10.25]
    concordance_threshold = 0.6

    verbose = True
    w = WeightedSum(data=data, verbose=verbose)
    pa = Pareto(data=data, verbose=verbose)
    pr = Promethee(data=data, verbose=verbose)
    e = Electre(data=data, verbose=verbose)

    # print()
    # print()
    # print()
    # print('#'*79)
    # print('[PARETO]')
    # print('#'*79)
    # result = pa.solve(indexes=criteria_idx, prefs=criteria_prefs)
    # print(result)
    # print('#'*79)
    # print()
    # print()
    # print()
    # print('#'*79)
    # print('[WEIGHED SUM]')
    # print('#'*79)
    # result = w.solve(pref_indexes=criteria_idx, prefs=criteria_prefs, weights=criteria_weights, target='min')
    # print(result)
    # print('#'*79)
    # print()
    # print()
    # print()
    # print('#'*79)
    # print('[PROMETHEE]')
    # print('#'*79)
    # result = pr.solve(weights=weights, prefs=prefs)
    # print(result)
    # print('#'*79)
    print()
    print()
    print()
    print('#'*79)
    print('[ELECTRE]')
    print('#'*79)
    result = e.solve(weights, prefs, vetoes, concordance_threshold, preference_thresholds)
    # print(result)
    print('#'*79)