"""
Methods for numerical fitting of data.
"""

from ..fit import *

from ._find_beta import _find_beta

from ._odr_fit import _odr_fit

from . import minimize
from .minimize import *

__all__ = ['fit']

