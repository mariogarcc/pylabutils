import warnings

import numpy as np
# try to get rid of numpy

def _sqerr_sum(_func_image, xdata, ydata, *parms):
    """
    Computes the sum of squared errors for some data, using _func_image format.
    """
    image = _func_image(xdata, *parms)
    # note how this only takes x and parameters: this is the _func_image format
    return np.sum((ydata - image) ** 2.0)
