

[![PyPI version](https://badge.fury.io/py/EasyMCDM.svg)](https://badge.fury.io/py/EasyMCDM)
[![GitHub Issues](https://img.shields.io/github/issues/qanastek/EasyMCDM.svg)](https://github.com/qanastek/EasyMCDM/issues)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
<!-- [![Downloads](https://static.pepy.tech/personalized-badge/EasyMCDM?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/EasyMCDM) -->

# Quick installation

# EasyMCDM - Install

## Install with PyPI

Once you have created your Python environment (Python 3.6+) you can simply type:

```bash
pip3 install EasyMCDM
```

## Install with GitHub

Once you have created your Python environment (Python 3.6+) you can simply type:

```bash
git clone https://github.com/qanastek/EasyMCDM.git
cd EasyMCDM
pip3 install -r requirements.txt
pip3 install --editable .
```

Any modification made to the `EasyMCDM` package will be automatically interpreted as we installed it with the `--editable` flag.


## Setup with Anaconda 

```bash
conda create --name EasyMCDM python=3.6 -y
conda activate EasyMCDM
```

More information on managing environments with Anaconda can be found in [the conda cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).


# Try It

**Promethee :**

```python
from EasyMCDM.models.Promethee import Promethee

data = pd.read_csv('tests/data/donnees.csv', header=None).to_numpy()
# or
data = {
  "alfa_156": [23817.0, 201.0, 8.0, 39.6, 6.0, 378.0, 31.2],
  "audi_a4": [25771.0, 195.0, 5.7, 35.8, 7.0, 440.0, 33.0],
  "cit_xantia": [25496.0, 195.0, 7.9, 37.0, 2.0, 480.0, 34.0]
}
weights = [0.14,0.14,0.14,0.14,0.14,0.14,0.14]
prefs = ["min","max","min","min","min","max","min"]

p = Promethee(data=data, verbose=False)
res = p.solve(weights=weights, prefs=prefs)
print(res)
```

**Electre Iv / Is :**

```python
from EasyMCDM.models.Electre import Electre

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
preference_thresholds = [20, 10, 200, 4, 2, 2] # or None for Electre Iv

e = Electre(data=data, verbose=False)

results = e.solve(weights, prefs, vetoes, indifference_threshold, preference_thresholds)
```

**Pareto :**

```python
from EasyMCDM.models.Pareto import Pareto

data = 'tests/data/donnees.csv'
# or
data = {
  "alfa_156": [23817.0, 201.0, 8.0, 39.6, 6.0, 378.0, 31.2],
  "audi_a4": [25771.0, 195.0, 5.7, 35.8, 7.0, 440.0, 33.0],
  "cit_xantia": [25496.0, 195.0, 7.9, 37.0, 2.0, 480.0, 34.0]
}

p = Pareto(data=data, verbose=False)
res = p.solve(indexes=[0,1,6], prefs=["min","max","min"])
print(res)
```

**Weighted Sum :**
```python
from EasyMCDM.models.WSum import WSum

data = 'tests/data/donnees.csv'
# or
data = {
  "alfa_156": [23817.0, 201.0, 8.0, 39.6, 6.0, 378.0, 31.2],
  "audi_a4": [25771.0, 195.0, 5.7, 35.8, 7.0, 440.0, 33.0],
  "cit_xantia": [25496.0, 195.0, 7.9, 37.0, 2.0, 480.0, 34.0]
}

p = WSum(data=data, verbose=False)
res = p.solve(pref_indexes=[0,1,6],prefs=["min","max","min"], weights=[0.001,2,3], target='min')
print(res)
```


Data in `tests/data/donnees.csv` :

```csv
alfa_156,23817,201,8,39.6,6,378,31.2
audi_a4,25771,195,5.7,35.8,7,440,33
cit_xantia,25496,195,7.9,37,2,480,34
```

# List of methods available

- [Promethee I](https://www.sciencedirect.com/science/article/pii/S0098300411004365)
- [Promethee II](https://www.sciencedirect.com/science/article/pii/S0098300411004365)
- [Electre Iv](https://en.wikipedia.org/wiki/%C3%89LECTRE)
- [Electre Is](https://en.wikipedia.org/wiki/%C3%89LECTRE)
- [Pareto](https://www.sciencedirect.com/topics/engineering/pareto-optimality)

# Build PyPi package

Build: `python setup.py sdist bdist_wheel`

Upload: `twine upload dist/*`

# Citation

If you want to cite the tool you can use this:

```bibtex
@misc{EasyMCDM,
  title={EasyMCDM},
  author={Yanis Labrak, Quentin Raymondaud, Philippe Turcotte},
  publisher={GitHub},
  journal={GitHub repository},
  howpublished={\url{https://github.com/qanastek/EasyMCDM}},
  year={2022}
}
```
