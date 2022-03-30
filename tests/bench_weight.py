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

paddings = []
weighted_values = []

nbindiv=500000
for i in range(10,nbindiv,100000):
    print(i)

    paddings.append(i)
    for j in range(i,i+100):
        data[str(j)] = [4.0, 5.0, 18.0, 39.6, 6.0, 378.0, 31.2]

    w = WeightedSum(data=data, verbose=False)


    start = time.time()
    rw = w.solve(pref_indexes=indexes, prefs=prefs, weights=weights, target='min')
    weighted_values.append(time.time() - start)

plt.plot(paddings, weighted_values, label="weighted")
plt.legend()
plt.savefig("wbenchmark_nb_indiv.png")
plt.close()

nbindiv=200
nbcrit=500000

paddings = []
weighted_values = []

for i in range(10,nbcrit,100000):

    print(i)
    data={}
    for j in range(nbindiv):
        data[str(j)] = [ nbcrit-j for j in range(i) ]
    indexes = [ j for j in range(i) ]
    weights = [ 1/i for j in range(i)]
    prefs = ["min" for j in range(i)]
    paddings.append(i)

    w = WeightedSum(data=data, verbose=False)

    start = time.time()
    rw = w.solve(pref_indexes=indexes, prefs=prefs, weights=weights, target='min')
    weighted_values.append(time.time() - start)

plt.plot(paddings, weighted_values, label="weighted")
plt.legend()
plt.savefig("wbenchmark_nb_crit.png")