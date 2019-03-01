"""
Some tools to have some methods delegated to outside functions for clear code.
"""

from ._colors import color_dict
from ._add_cols import _add_cols
from ._ffixx import _ffixx
from ._get_image import _get_image
from ._ms_methods import *
# from ._imports import *

__all__ = ['color_dict', '_add_cols', 'ms_methods']