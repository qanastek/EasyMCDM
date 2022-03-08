import os
import glob
from os.path import dirname, basename, isfile, join

from . import utils
from . import models

with open(os.path.join(dirname(__file__), "version.txt")) as f:
    version = f.read().strip()

__version__ = version
