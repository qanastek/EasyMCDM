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
        "peugeot_406":  [25649.0, 191.0, 8.3, 34.4, 2.0, 430.0, 34.6], 
        "vw_passat":    [23344.0, 195.0, 7.6, 34.4, 3.0, 475.0, 33.6], 
        "rnlt_safrane": [29160.0, 203.0, 7.5, 34.5, 1.0, 520.0, 32.0],
        "saab_tid":     [26183.0, 199.0, 7.8, 35.7, 5.0, 494.0, 32.0], 
        "audi_a4":      [25771.0, 195.0, 5.7, 35.8, 7.0, 440.0, 33.0], 
        "bmw_320d":     [26260.0, 209.0, 6.6, 36.6, 4.0, 440.0, 30.9], 
        "cit_xantia":   [25496.0, 195.0, 7.9, 37.0, 2.0, 480.0, 34.0], 
        "rnlt_laguna":  [23664.0, 194.0, 7.7, 37.4, 4.0, 452.0, 33.8], 
        "alfa_156":     [23817.0, 201.0, 8.0, 39.6, 6.0, 378.0, 31.2], 
        "cit_xsara":    [19084.0, 182.0, 6.4, 40.6, 8.0, 408.0, 33.5], 
    }
    # criteria_idx =          [    4,     2,     0]
    # criteria_prefs =        ["min", "min", "min"]
    # criteria_weights =      [ 0.25,  0.25,  0.5]
    criteria_idx =          [    4,     2,     5]
    criteria_prefs =        ["min", "min", "max"]
    criteria_weights =      [ 0.55,  0.25,  0.20]
    weight_idx =            [      0,     1,     2,     3,     4,     5,     6]
    weights =               [   0.10,  0.00,  0.25,  0.05,  0.40,  0.20,  0.00]
    prefs =                 [  "min", "max", "min", "min", "min", "max", "min"]
    # preference_thresholds = None
    preference_thresholds = [ 7500.00,  0.00, 1.75, 1.50, 3.00, 55.00,  0.00]
    # Respected vetos indicate non-discordance, which means more outranking and smaller kernels.
    #   - Raise vetos for positive (desirable) criteria.
    # Broken vetos indicate discordance and absense of outranking, which means less outranking and larger kernels.
    #   - Lower vetos for negative (undesirable) criteria.
    # Vetos regulate discordance (broken) or non-discordance (respected).
    vetoes =                [11000.00,  0.00, 2.00, 4.00, 5.00, 85.00, 0.00]
    # Lower concordance tresholds and/or smaller vetos (less 1s), lead to less outranking (links in graph) and larger kernels.
    # Higher concordance tresholds and larger vetos (more 1s), lead to more outranking (links in graph) and smaller kernels.
    concordance_threshold = 0.75

    verbose = True
    w  = WeightedSum(data=data, verbose=verbose)
    pa = Pareto(data=data, verbose=verbose)
    pr = Promethee(data=data, verbose=verbose)
    e  = Electre(data=data, verbose=verbose)

    # print()
    # print()
    # print()
    # print('#'*79)
    # print('[PARETO]')
    # print('#'*79)
    # result = pa.solve(indexes=criteria_idx, prefs=criteria_prefs)
    # print(result)
    # print('#'*79)
    print()
    print()
    print()
    print('#'*79)
    print('[WEIGHED SUM]')
    print('#'*79)
    result = w.solve(pref_indexes=weight_idx, prefs=prefs, weights=weights, target='min')
    print(result)
    print('#'*79)
    print()
    print()
    print()
    print('#'*79)
    print('[PROMETHEE]')
    print('#'*79)
    result = pr.solve(weights=weights, prefs=prefs)
    print('#'*79)
    print()
    print()
    print()
    print('#'*79)
    print('[ELECTRE]')
    print('#'*79)
    result = e.solve(weights, prefs, vetoes, concordance_threshold, preference_thresholds)
    print('#'*79)