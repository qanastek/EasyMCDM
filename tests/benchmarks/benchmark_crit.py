import time
import matplotlib.pyplot as plt

from EasyMCDM.models.Electre import Electre
from EasyMCDM.models.Promethee import Promethee
from EasyMCDM.models.Pareto import Pareto
from EasyMCDM.models.WeightedSum import WeightedSum
from EasyMCDM.models.Irmo import Irmo

data = {}
indexes = [ 0, 1, 2, 3, 4, 5, 6 ]
weights = [0.14,0.14,0.14,0.14,0.14,0.14,0.14]
prefs = ["min","max","min","min","min","max","min"]
vetoes = [45, 29, 550, 6, 4.5, 4.5, 4.5]
indifference_threshold = 0.6
preference_thresholds = [20, 10, 200, 4, 2, 2, 7]

paddings = []
promethee_values = []
electre_values = []
weighted_values = []
pareto_values = []

data = {}
nbindiv=200
nbcrit=2000

paddings = []
promethee_values = []
electre_values = []
weighted_values = []
pareto_values = []

for i in range(2,nbcrit,100):
    
    for j in range(nbindiv):
        data[str(j)] = [ 5 for j in range(i) ]
        
    print(i)
    indexes = [ j for j in range(i) ]
    weights = [ 1/i for j in range(i)]
    prefs = ["min" for j in range(i)]
    vetoes = [5 for j in range(i)]
    indifference_threshold = 0.6
    preference_thresholds = [20 for j in range(i)]
    paddings.append(i)

    print(len(indexes))
    print(len(weights))
    print(len(prefs))
    print(len(vetoes))
    print(len(preference_thresholds))
    print(len(data["0"]))
    print(len(data))
    print()

    w = WeightedSum(data=data, verbose=False)
    pa = Pareto(data=data, verbose=False)
    pr = Promethee(data=data, verbose=False)
    e = Electre(data=data, verbose=False)

    start = time.time()
    re = e.solve(weights, prefs, vetoes, indifference_threshold, preference_thresholds)
    electre_values.append(time.time() - start)

    start = time.time()
    rpr = pr.solve(weights=weights, prefs=prefs)
    promethee_values.append(time.time() - start)

    start = time.time()
    rpa = pa.solve(indexes=indexes, prefs=prefs)
    pareto_values.append(time.time() - start)

    start = time.time()
    rw = w.solve(pref_indexes=indexes, prefs=prefs, weights=weights, target='min')
    weighted_values.append(time.time() - start)

plt.plot(paddings, promethee_values, label="promethee")
plt.plot(paddings, electre_values, label="electre")
plt.plot(paddings, weighted_values, label="weighted")
plt.plot(paddings, pareto_values, label="pareto")
plt.legend()
plt.savefig("benchmark_nb_crit.png")