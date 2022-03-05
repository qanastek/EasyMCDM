#!/usr/bin/env python3
import os
import setuptools
from distutils.core import setup

with open("README.md") as f:
    long_description = f.read()

with open(os.path.join("EasyMCDM", "version.txt")) as f:
    version = f.read().strip()

setup(
    name = "EasyMCDM",
    version = version,
    description = "A easy to use Multi-Criteria Decision-Making (MCDM) toolkit which propose implementations for Electre, Promethee and much more.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = "Yanis Labrak & Others",
    author_email = "yanis.labrak@univ-avignon.fr",
    packages = setuptools.find_packages(),
    package_data = {
        "EasyMCDM": [
            "version.txt"
        ]
    },
    install_requires = [
        "numpy",
        "pandas",
        "prettytable",
    ],
    python_requires = ">=3.6",
    url = "https://EasyMCDM.github.io/",
    keywords = ["python","MCDM","toolkit","easy","Multiple-criteria decision analysis","Multi-Criteria Decision-Making","methods","Multi-Criteria Decision-Making (MCDM)"],
)