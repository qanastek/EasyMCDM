[![PyPI version](https://badge.fury.io/py/EasyMCDM.svg)](https://badge.fury.io/py/EasyMCDM)
[![GitHub Issues](https://img.shields.io/github/issues/qanastek/EasyMCDM.svg)](https://github.com/qanastek/EasyMCDM/issues)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
<!-- [![Downloads](https://static.pepy.tech/personalized-badge/EasyMCDM?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/EasyMCDM) -->

# EasyMCDM - Quick Installation methods

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

Data in `tests/data/donnees.csv` :

```csv
alfa_156,23817,201,8,39.6,6,378,31.2
audi_a4,25771,195,5.7,35.8,7,440,33
cit_xantia,25496,195,7.9,37,2,480,34
```

## Promethee

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

**Output :**

```python
{
  'phi_negative': [('rnlt_safrane', 2.381), ('vw_passat', 2.9404), ('bmw_320d', 3.3603), ('saab_tid', 3.921), ('audi_a4', 4.34), ('cit_xantia', 4.48), ('rnlt_laguna', 5.04), ('alfa_156', 5.32), ('peugeot_406', 5.461), ('cit_xsara', 5.741)],
  'phi_positive': [('rnlt_safrane', 6.301), ('vw_passat', 5.462), ('bmw_320d', 5.18), ('saab_tid', 4.76), ('audi_a4', 4.0605), ('cit_xantia', 3.921), ('rnlt_laguna', 3.6406), ('alfa_156', 3.501), ('peugeot_406', 3.08), ('cit_xsara', 3.08)],
  'phi': [('rnlt_safrane', 3.92), ('vw_passat', 2.5214), ('bmw_320d', 1.8194), ('saab_tid', 0.839), ('audi_a4', -0.27936), ('cit_xantia', -0.5596), ('rnlt_laguna', -1.3995), ('alfa_156', -1.8194), ('peugeot_406', -2.381), ('cit_xsara', -2.661)],
  'matrix': '...'
}
```

## Electre Iv / Is

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

**Output :**

```python
{'kernels': ['A4', 'A5']}
```

## Pareto

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

**Output :**

```python
{
  'alfa_156': {'Weakly-dominated-by': [], 'Dominated-by': []},
  'audi_a4': {'Weakly-dominated-by': ['alfa_156'], 'Dominated-by': ['alfa_156']}, 
  'cit_xantia': {'Weakly-dominated-by': ['alfa_156', 'vw_passat'], 'Dominated-by': ['alfa_156']},
  'peugeot_406': {'Weakly-dominated-by': ['alfa_156', 'cit_xantia', 'rnlt_laguna', 'vw_passat'], 'Dominated-by': ['alfa_156', 'cit_xantia', 'rnlt_laguna', 'vw_passat']},
  'saab_tid': {'Weakly-dominated-by': ['alfa_156'], 'Dominated-by': ['alfa_156']}, 
  'rnlt_laguna': {'Weakly-dominated-by': ['vw_passat'], 'Dominated-by': ['vw_passat']}, 
  'vw_passat': {'Weakly-dominated-by': [], 'Dominated-by': []},
  'bmw_320d': {'Weakly-dominated-by': [], 'Dominated-by': []},
  'cit_xsara': {'Weakly-dominated-by': [], 'Dominated-by': []},
  'rnlt_safrane': {'Weakly-dominated-by': ['bmw_320d'], 'Dominated-by': ['bmw_320d']}
}
```

## Weighted Sum

```python
from EasyMCDM.models.WeightedSum import WeightedSum

data = 'tests/data/donnees.csv'
# or
data = {
  "alfa_156": [23817.0, 201.0, 8.0, 39.6, 6.0, 378.0, 31.2],
  "audi_a4": [25771.0, 195.0, 5.7, 35.8, 7.0, 440.0, 33.0],
  "cit_xantia": [25496.0, 195.0, 7.9, 37.0, 2.0, 480.0, 34.0]
}

p = WeightedSum(data=data, verbose=False)
res = p.solve(pref_indexes=[0,1,6],prefs=["min","max","min"], weights=[0.001,2,3], target='min')
print(res)
```

**Output :**

```python
[(1, 'bmw_320d', -299.04), (2, 'alfa_156', -284.58299999999997), (3, 'rnlt_safrane', -280.84), (4, 'saab_tid', -275.817), (5, 'vw_passat', -265.856), (6, 'audi_a4', -265.229), (7, 'rnlt_laguna', -262.93600000000004), (8, 'cit_xantia', -262.504), (9, 'peugeot_406', -252.551), (10, 'cit_xsara', -244.416)]
```

## Instant-Runoff Multicriteria Optimization (IRMO)

```python
from EasyMCDM.models.Irmo import Irmo

p = Irmo(data="data/donnees.csv", verbose=False)
res = p.solve(
    indexes=[0,1,4,5], # price -> max_speed -> comfort -> trunk_space
    prefs=["min","max","min","max"]
)
print(res)
```

**Output :**

```python
{'best': 'saab_tid'}
```


# List of methods available

- [Promethee I](https://www.sciencedirect.com/science/article/pii/S0098300411004365)
- [Promethee II](https://www.sciencedirect.com/science/article/pii/S0098300411004365)
- [Electre Iv](https://en.wikipedia.org/wiki/%C3%89LECTRE)
- [Electre Is](https://en.wikipedia.org/wiki/%C3%89LECTRE)
- [Weighted Sum](https://en.wikipedia.org/wiki/Weighted_sum_model)
- [Pareto](https://www.sciencedirect.com/topics/engineering/pareto-optimality)
- Instant-Runoff Multicriteria Optimization (IRMO)

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
