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

nbindiv=2500
for i in range(10,nbindiv,100):
    print(i)

    paddings.append(i)
    for j in range(i,i+100):
        data["item_" + str(j)] = [4.0, 5.0, 18.0, 39.6, 6.0, 378.0, 31.2]

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
plt.savefig("benchmark_nb_indiv.png")
plt.close()
