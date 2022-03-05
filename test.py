import pandas as pd
from Promethee import Promethee

d = pd.read_csv('data/donnees.csv', header=None).to_numpy()
d = "data/donnees.csv"
d = { "alfa_156": [23817.0, 201.0, 8.0, 39.6, 6.0, 378.0, 31.2], "audi_a4": [25771.0, 195.0, 5.7, 35.8, 7.0, 440.0, 33.0], "cit_xantia": [25496.0, 195.0, 7.9, 37.0, 2.0, 480.0, 34.0], "peugeot_406": [25649.0, 191.0, 8.3, 34.4, 2.0, 430.0, 34.6], "saab_tid": [26183.0, 199.0, 7.8, 35.7, 5.0, 494.0, 32.0], "rnlt_laguna": [23664.0, 194.0, 7.7, 37.4, 4.0, 452.0, 33.8], "vw_passat": [23344.0, 195.0, 7.6, 34.4, 3.0, 475.0, 33.6], "bmw_320d": [26260.0, 209.0, 6.6, 36.6, 4.0, 440.0, 30.9], "cit_xsara": [19084.0, 182.0, 6.4, 40.6, 8.0, 408.0, 33.5], "rnlt_safrane": [29160.0, 203.0, 7.5, 34.5, 1.0, 520.0, 32.0] }

w = "data/weights.txt"
w = [0.14,0.14,0.14,0.14,0.14,0.14,0.14]

prefs = "data/preferences.txt"
prefs = ["min","max","min","min","min","max","min"]

p = Promethee()
res = p.solve(data=d, weights=w, prefs=prefs)

# All values of phi
assert ('rnlt_safrane', 2.5200000000000005) == res["phi_negative"][0], "✔️ phi_negative assert failed!"
assert ('rnlt_safrane', 6.300000000000001) == res["phi_positive"][0], "✔️ phi_positive assert failed!"
assert ('rnlt_safrane', 3.7800000000000002) == res["phi"][0], "✔️ phi assert failed!"

# Matrix
matrix = open("asserts/matrix.txt","r").read()
assert matrix == res["matrix"], "✔️ matrix assert failed!"

print("✔️Success ! All the asserts are okay!")
