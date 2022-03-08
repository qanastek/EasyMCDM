

[![PyPI version](https://badge.fury.io/py/EasyMCDM.svg)](https://badge.fury.io/py/EasyMCDM)
[![GitHub Issues](https://img.shields.io/github/issues/qanastek/EasyMCDM.svg)](https://github.com/qanastek/EasyMCDM/issues)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
<!-- [![Downloads](https://static.pepy.tech/personalized-badge/EasyMCDM?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/EasyMCDM) -->

# Quick installation

## Anaconda setup

```bash
conda create --name EasyMCDM python=3.6 -y
conda activate EasyMCDM
```

More information on managing environments with Anaconda can be found in [the conda cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).

## Install via PyPI

Once you have created your Python environment (Python 3.6+) you can simply type:

```bash
pip install EasyMCDM
```

## Install with GitHub

Once you have created your Python environment (Python 3.6+) you can simply type:

```bash
git clone https://github.com/qanastek/EasyMCDM.git
cd EasyMCDM
pip install -r requirements.txt
pip install --editable .
```

Any modification made to the `EasyMCDM` package will be automatically interpreted as we installed it with the `--editable` flag.

# Try It

```python
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

Data in `tests/data/donnees.csv` :

```csv
alfa_156,23817,201,8,39.6,6,378,31.2
audi_a4,25771,195,5.7,35.8,7,440,33
cit_xantia,25496,195,7.9,37,2,480,34
```

# List of methods available :

- [Promethee II](https://www.sciencedirect.com/science/article/pii/S0098300411004365)
- [Electre Iv](https://en.wikipedia.org/wiki/%C3%89LECTRE) (Coming soon)
- [Pareto](https://www.sciencedirect.com/topics/engineering/pareto-optimality) (Coming soon)

# Build PyPi package

Build: `python setup.py sdist bdist_wheel`

Upload: `twine upload dist/*`

# Citation

If you want to cite the tool you can use this:

```bibtex
@misc{EasyMCDM,
  title={EasyMCDM},
  author={Yanis Labrak},
  publisher={GitHub},
  journal={GitHub repository},
  howpublished={\url{https://github.com/qanastek/EasyMCDM}},
  year={2022}
}
```
