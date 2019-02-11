__all__ = ['fit']

import re
import copy
import numpy as np
import scipy.optimize as so
import matplotlib.pyplot as plt

from matplotlib import rc

from .._colors import color_dict
from .._tools import _get_image, _ffixx, _plot_fit

from ..utils.io import _print_measure


###############################################################
"""
===============================================================
"""
###############################################################


def _sqerrSum(_func_image, xdata, ydata, *parms):
    """
    """
    warnings.filterwarnings("ignore")
    image = _func_image(xdata, *parms)
    # note how this only takes x and parameters!
    # equivalent to _func_image in the main fit() function
    return np.sum((ydata - image) ** 2.0)


###############################################################
"""
===============================================================
"""
###############################################################


def _find_beta(func, xdata, ydata, min_func, nparms, **options):
    """
    """

    kw = dict(
        bounds = (-1000, 1000),
        fb_method = 'differential_evolution',
        de_strategy = 'best1bin',
        de_maxiter = None,
        de_popsize = 15,
        de_tol = 0.01,
        de_mutation = (0.5, 1),
        de_recombination = 0.7,
        de_seed = None,
        de_callback = None,
        de_disp = False,
        de_polish = True,
        de_init = 'latinhypercube',
    )

    kw.update(options)

    if kw['fb_method'].lower() == 'differential_evolution':
        try:
            x_max, y_max = max(xdata), max(ydata)
            x_min, y_min = min(xdata), min(ydata)
            xy_max, xy_min = max(x_max, y_max), min(x_min, x_min)
            if kw['bounds'] == None or kw['bounds'] == (-np.inf, np.inf):
                kw['bounds'] = [[-xy_max, xy_max]] * nparms
            elif len(kw['bounds']) == 2 \
                    and type(kw['bounds'] not in (list, tuple)):
                kw['bounds'] = [kw['bounds']] * nparms

            result = so.differential_evolution(
                min_func,
                kw['bounds'],
                strategy = kw['de_strategy'],
                maxiter = kw['de_maxiter'],
                popsize = kw['de_popsize'],
                tol = kw['de_tol'],
                mutation = kw['de_mutation'],
                recombination = kw['de_recombination'],
                seed = kw['de_seed'],
                callback = kw['de_callback'],
                disp = kw['de_disp'],
                polish = kw['de_polish'],
                init = kw['de_init'],
            )
        except:
            raise ValueError("couldn't find beta")

        return result.x

    else:
        print("{!r} is not implemented yet".format(kw['fb_method']))
        return

    return


###############################################################
"""
===============================================================
"""
###############################################################

def fit(func, xdata, ydata, **options):
    """
    Adjusts (x, y) data to a given curve with unknown parameter values with
    optional convenient result graphing.

    > Parameters:

    func : *string*
    Equation of the curve the data is to be compared against. Must be of the
    form 'y = f(x)' meaning that the first term has to be left alone, with no
    operations applied onto it (e.g. 1/y). 'y', however, can have an arbitrary
    name, such as 'q', 'theta', etc. 'x' can also have an arbitrary name but
    that name must be either enclosed between square brackets **or** specified
    in the `custom_x` option. If this is the case, avoid using variables
    named 'x'.
    The function will theoretically have some parameters that will have to
    be found for the data to be fit to the curve. Those parameters must be
    written between curly brackets `{ }`,
    e.g.:
        'y = {A} * numpy.exp( x * {B} ) + {C}',
        'y = {C_2} * x ** 2 + {C_1} * x + {C_0}'

    xdata : *array-like*
    x-axis data.

    y : *array-like*
    y-axis data.

    yerr : *array-like; optional*
    y-data values' deviation. Provides insight on how the data should be fit.
    default : None

    xerr : *array-like; optional*
    x-data values' deviation. In this function, this argument is only for
    graphical purposes. For an implementation into the data fit see the
    odr_fit function.
    default : None

    fit_method : *{'simple', 'odr'}; optional*
    Determines what method is going to be used to fit the parameters to the
    function. ODR takes `xerr` values into account.
    default : 'simple'

    beta0 : *N x scalar; optional*
    Sets a first guess for function parameters. N is the number of function
    parameters. Might be required if the function fails to find the correct
    parameters; throws `RuntimeError`.
    default : 0. x N

    absolute_err : *bool; optional*
    Specifies whether the `yerr` provided is in absolute or relative values.
    default : True

    bounds : *2-tuple of array-like; optional*
    Lower and upper bounds of parameter values. Each element of the tuple must
    be either an array with the length equal to the number of parameters, or
    a scalar (in which case the bound is taken to be the same for all
    parameters.) Use np.inf with an appropriate sign to disable bounds on all
    or some parameters.
    default : (-np.inf, np.inf)

    simple_method : *{'lm', 'trf', 'dogbox'}; optional*
    Method to use for optimization when using `fit_method = 'simple'`.
    See (https://docs.scipy.org/doc/scipy/
    reference/generated/scipy.optimize.curve_fit.html) for more details.
    default : None

    graph : *M x bool or bool; optional*
    Chooses whether to show graphical representations for any of the three
    graphical options: the first graph plots the data given, the second graph
    plots the curve corresponding to the function after the parameters have
    been found via `numpy.linspace`, and the third graph plots xdata vs. the
    image of xdata through the given function after the values of the
    parameters have been found.
    If True, only the first two graphs will be created.
    default : False

    errorbars : *bool; optional*
    Chooses whether to show error caps on the corresponding graphs.
    default : True

    sizes : *M x 2 x scalar; optional*
    Sets `matplotlib.figure.Figure.figsize` for the graphical representations.
    default : 3 x (6, 4)

    split : *bool; optional*
    Chooses whether to split the data representation into separate graphs.
    default : True

    save : *bool or str or M x str; optional*
    Chooses whether to save the files with a default name or give them a custom
    one. If it is a string, different file names will be created based on the
    type of graph.
    default : False

    colors : *M x str, RGB or color name supported in color_dict; optional*
    Chooses what colors to use in the different graphs.
    default : ['blue', 'red', 'orange']

    usetex : *bool; optional*
    Chooses whether to use the TeX engine to render text inside the graphs.
    default : True

    font_family : *str; optional*
    Specifies which font family the TeX engine will use when rendering text.
    default : 'serif'

    axis_labels : *2 x str; optional*
    Labels the two axis of the graphs. Note that they are shared.
    default : [None, None]

    legend : *bool or str; optional*
    Chooses whether to display the legend for the graph. If str, specifies the
    legend location. If True, location is set to 'best'. Valid arguments are
    those specified in the `matplotlib.pyplot.legend`
    default : False

    linspace_vals : *scalar; optional*
    Specifies the amount of `numpy.linspace` points to be displayed in the
    curve graph.
    default : 400

    custom_x : *str; optional*
    Specifies which string is to be interpreted as the 'x' variable inside
    the function. The default string is 'x'. It is recommended to use square
    brackets instead of this option.
    default : False (no custom_x string)

    printf : *bool; optional*
    Chooses whether to print the function with the found parameter values.
    default : False

    res_fmt : *str; optional*
    Specifies string formatting when printing parameter results. Options are
    the same as mentioned in the docs for the `uncertainties` package @
    https://
    uncertainties-python-package.readthedocs.io/en/latest/user_guide.html
    #printing
    If let as default, any number greater than 1000 or less than 0.01 will
    change the formatting to exponential form.
    default : '.2uL' -> 2 significance digits for uncertainty, LaTeX output

    > Other options:

    capsize, titles, labels, markers, linestyles, ecolor, elinewidth,
    errorevery, barsabove, linewitdh, markersize, markevery, fillstyle,
    jfit_type, jderiv, jvar_calc, jdel_init, jrestart, de_strategy,
    de_maxiter, de_popsize, de_tol, de_mutation, de_recombination,
    de_seed, de_callback, de_disp, de_polish, de_init.

    For information about the options just mentioned, please refer to the
    following documentations:
    `matplotlib.pyplot.errorbar`,
    `scipy.optimize.differential_evolution`,
    `scipy.odr.set_job`

    """

    whole_func = copy.deepcopy(func)
    func = copy.deepcopy(func)[func.find('=')+1:]

    parms = re.findall(r'(?<=\{)\w[\w\.\(\)]*(?=\})', func)
    # finds parameters to adjust

    for parm in parms:
        if parms.count(parm) > 1:
            temp = parms[::-1]
            temp.remove(parm)
            parms = temp[::-1].copy()
    # removes all duplicates from the end back

    kwargs = dict(
        yerr = None,
        xerr = None,
        beta0 = 'find',
        absolute_err = True,
        bounds = (-np.inf, np.inf),
        fit_method = 'simple',
        simple_method = None,
        graph = False,
        errorbars = True,
        sizes = [(6, 4), (6, 4), (6, 4)],
        split = True,
        save = False,
        colors = ['blue', 'red', 'orange'],
        capsize = 3,
        titles = [None, None, None],
        labels = [None, None, None],
        axis_labels = [None, None],
        legend = False,
        markers = ['.', '', '.'],
        linestyles = ['', '-', ''],
        ecolor = None,
        elinewidth = None,
        errorevery = 1,
        barsabove = False,
        linspace_vals = 400,
        linewidth = 1.5,
        markersize = 6.0,
        markevery = 1,
        fillstyle = 'full',
        usetex = True,
        font_family = 'serif',
        custom_x = False,
        printf = False,
        res_fmt = '.2uL',
        jfit_type = None, # odr kwargs
        jderiv = None,
        jvar_calc = None,
        jdel_init = None,
        jrestart = None, #
        de_func = _sqerrSum, #differential_evolution kwargs
        # this ^ kwarg is weird,  I'll have to explain
        de_strategy = 'best1bin',
        de_maxiter = None,
        de_popsize = 15,
        de_tol = 0.01,
        de_mutation = (0.5, 1),
        de_recombination = 0.7,
        de_seed = None,
        de_callback = None,
        de_disp = False,
        de_polish = True,
        de_init = 'latinhypercube', #
    ) # default kwargs values

    defaults = kwargs
    kwargs.update(options) # changes kwargs values to fit kwargs input

    # checks if list kwargs are introduced accordingly
    if len([graph == True for graph in (kwargs['graph'] if \
            type(kwargs['graph']) == list else [kwargs['graph']])]) == 1:
        for option in ['sizes', 'colors', 'titles', 'labels', 'markers', \
                'linestyles']:
            if type(kwargs[option]) != list:
                kwargs[option] = list(kwargs[option])

    # setting rcParams
    plt.rc('text', usetex = kwargs['usetex'])
    plt.rc('font', family = kwargs['font_family'])

    # changing custom independent variable to 'x' to work with it later
    func = _ffixx(func, kwargs['custom_x'])

    def _func_image(x, *values):
        return _get_image(x, *values, func_str = func, parms = parms)
    # nice workaround :-)

    if kwargs['beta0'] == 'find':
        def _de_func(values):
            return kwargs['de_func'](_func_image,
                np.array(xdata), np.array(ydata), *values)
            # !!!!!! the last parameter *values* -- this is VERY confusing

        try:
            kwargs['beta0'] = \
                _find_beta(_func_image, xdata, ydata, _de_func, len(parms))
                # maybe change the nparms requirement other day
        except:
            print("Setting beta0 to [1.] * len(parms)")
            kwargs['beta0'] = [1.] * len(parms)


    if kwargs['fit_method'].lower() == 'simple':
        # simple method
        sols = so.curve_fit(
            _func_image, xdata, ydata,
            p0 = kwargs['beta0'],
            sigma = kwargs['yerr'],
            absolute_sigma = kwargs['absolute_err'],
            bounds = kwargs['bounds'],
            method = kwargs['simple_method']
            )

        fit_parms = sols[0]
        fit_parms_us = np.sqrt(np.diag(sols[1]))


    elif kwargs['fit_method'].lower() == 'odr':

        fit_parms, fit_parms_us = \
            _odr_fit(_func_image, xdata, ydata, kwargs['beta0'], **kwargs)


    # results

    # if introducing uncertainties module:
    # which is now required
    # fit_parm_pairs = \
    #   [us.ufloat(parm, u) for parm, u in zip(fit_parms, fit_parms_us)
    # ... etc.

    # fit_parms = [us.ufloat(parm, u) \
    #    for parm, u in zip(fit_parm, fit_parms_us)]

    fit_func = copy.deepcopy(func)
    for i in range(len(fit_parms)):
        fit_func = re.sub( \
            '{{{}}}'.format(parms[i]), str(fit_parms[i]), fit_func)

    xloc = re.search(r'[^\w\.]x[^\w\.]', fit_func).start() + 1
    tempf = [fit_func[i] if i != xloc else 'xdata' \
        for i in range(len(fit_func))]
    fit_func = copy.deepcopy(''.join(tempf))
    # string for the resulting function with fit parameters
    # substituting xdata so that it is called when fit_curve is evaluated
    # fit_func = re.sub('x', 'xdata', fit_func) fails against np.exp, etc.

    # new: introducing uncertainties module as requirement (formatting only)
    for name, pair in zip(parms, zip(fit_parms, fit_parms_us)):
        _print_measure(pair[0], pair[1], name = name, fmt = kwargs['res_fmt'])

    # graph section
    # one graph has the data and the image points through the fit function
    # other graph has a dense curve, for graphic purposes
    if kwargs['graph'] == True:
        kwargs['graph'] = [True, True, False]

    if kwargs['graph'] != False and any(kwargs['graph']):
        _plot_fit(xdata, ydata, func_str = fit_func, **kwargs)

    # print the function?
    if kwargs['printf']:
        print_func = copy.deepcopy(whole_func)
        for i in range(len(fit_parms)):
            whole_func = re.sub( \
                '{{{}}}'.format(parms[i]), str(fit_parms[i]), print_func)
        print(whole_func)
        # possibility to print function with parameter uncertainties?
    # improvements could be made in all the function string naming and that...
    # returns [(parm, parm_unc), ...]
    return list(zip([fit_parms, fit_parms_us]))
