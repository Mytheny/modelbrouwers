try:
    from .secrets import *
except ImportError:
    import sys
    sys.exit('secrets.py settings file not found.')

from base import *


# for ease, override here. No production values are used anyway
SECRET_KEY = '04wb^^4e5%djxrpe4_u6*&ska+s(j1=!k2^frlfux2se#$%mox'