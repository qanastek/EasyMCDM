import os

from . import utils
from . import models

with open(os.path.join(os.path.dirname(__file__), "version.txt")) as f:
    version = f.read().strip()

__version__ = version