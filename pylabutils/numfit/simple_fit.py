import re
import copy
import numpy as np
import scipy.optimize as so
import matplotlib.pyplot as plt

from matplotlib import rc

from .._colors import color_dict

def simple_fit(func, xdata, ydata, **options):
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

    method : *{'lm', 'trf', 'dogbox'}; optional*
    Method to use for optimization. See (https://docs.scipy.org/doc/scipy/
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

    > Other options:

    capsize, titles, labels, markers, linestyles, ecolor, elinewidth,
    errorevery, barsabove, linewitdh, markersize, markevery, fillstyle.

    For information about the options just mentioned, please refer to the
    `matplotlib.pyplot.errorbar` documentation.

    """

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
        beta0 = [0.] * len(parms),
        absolute_err = True,
        bounds = (-np.inf, np.inf),
        method = None,
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
        fillstyle = 'full', ##############################################
        usetex = True,
        font_family = 'serif',
        custom_x = False,
        printf = False,
    ) # default kwargs values

    defaults = kwargs

    # add marker, linestyle, etc. kwargs? hm
    # add options to not be dual kwargs, like in table

    kwargs.update(options) # changes kwargs values to fit kwargs input

    if len([graph == True for graph in (kwargs['graph'] if \
            type(kwargs['graph']) == list else [kwargs['graph']])]) == 1:
        for option in ['sizes', 'colors', 'titles', 'labels', 'markers', \
                'linestyles']:
            if type(kwargs[option]) != list:
                kwargs[option] = list(kwargs[option])

    plt.rc('text', usetex = kwargs['usetex'])
    plt.rc('font', family = kwargs['font_family'])

    x_str = kwargs['custom_x'] if type(kwargs['custom_x']) == str else 'x'
    # square brackets notation overrides custom_x
    custom_x = re.search(r'(?<=\[)\w[\w\.\(\)]*(?=\])', func)
    if custom_x:
        x_str = func[custom_x.start():custom_x.end()]

    func = re.sub(r'\[{}\]'.format(x_str), 'x', func)

    def _func_image(x, *values):

        temp_curve = copy.deepcopy(func)

        for i in range(len(parms)):
            temp_curve = re.sub( \
                '{{{}}}'.format(parms[i]), str(values[i]), temp_curve)

        image = eval(temp_curve[temp_curve.find('=')+1:])

        return image

    sols = so.curve_fit(
        _func_image, xdata, ydata,
        p0 = kwargs['beta0'],
        sigma = kwargs['yerr'],
        absolute_sigma = kwargs['absolute_err'],
        bounds = kwargs['bounds'],
        method = kwargs['method']
        )
    # ydata no longer has an use

    fit_parms = sols[0]
    fit_parms_us = np.sqrt(np.diag(sols[1]))
    # results

    # if introducing uncertainties module:
    # fit_parm_pairs = \
    #   [us.ufloat(parm, u) for parm, u in zip(fit_parms, fit_parms_us)
    # ... etc.

    fit_func = copy.copy(func)
    for i in range(len(fit_parms)):
        fit_func = re.sub( \
            '{{{}}}'.format(parms[i]), str(fit_parms[i]), fit_func)

    xloc = re.search(r'[^\w\.]x[^\w\.]', fit_func).start() + 1
    tempf = [fit_func[i] if i != xloc else 'xdata' \
        for i in range(len(fit_func))]
    fit_func = copy.deepcopy(''.join(tempf))
    # string for the resulting function with fit parameters
    # substituting xdata so that it is called when fit_curve is evaluated
    # fit_func = re.sub('x', 'xdata', fit_func) fails against np.exp...

    fit_curve = fit_func[fit_func.find('=')+1:]
    # for eval() purposes

    try:
        if all([str(u) not in ['None', 'inf', 'INF', 'nan', 'NAN'] \
            for u in fit_parms_us]):
                significances = [
                    (re.search('[1-9]', str(u)).start()-2 \
                        if re.match('0\.', str(u)) \
                    else -re.search('\.', str(float(u))).start())+2 \
                    for u in fit_parms_us
                ]
                # two significant digits for uncertainty
        else:
            print('Uncertainty not found.')
            significances = [2] * len(fit_parms_us)
    except:
        raise('unexpected error')

    for i in range(len(fit_parms)):
        try:
            print(('{{0}} = {{1: {repr}}} ± {{2: {repr}}}'.format(
                repr = '1e' if fit_parms_us[i] >= 1000 \
                    else (
                        'd' if significances[i] <= 0 \
                        else '.{}f'.format(significances[i])
                    )
            )).format(
                parms[i],
                round(fit_parms[i], significances[i]),
                round(fit_parms_us[i], significances[i])
                ))
        except (TypeError, ValueError, OverflowError):
            print('some uncertainty value is invalid')
            continue
    # to get a peek on results

    # graph section
    # one graph has the data and the image points through the fit function
    # other graph has a dense curve, for graphic purposes

    if kwargs['graph'] == True:
        kwargs['graph'] = [True, True, False]

    if any(kwargs['graph']):

        xdata = np.array(xdata)
        xvals = np.linspace( \
            float(min(xdata)), float(max(xdata)), kwargs['linspace_vals'])

        if kwargs['errorbars']:
            yerr = np.array(kwargs['yerr']) if kwargs['yerr'] \
                is not None else None
            xerr = np.array(kwargs['xerr']) if kwargs['xerr'] \
                is not None else None

        dense_curve = re.sub('xdata', 'xvals', fit_curve)

        xs = [xdata, xvals, xdata]
        xerrs = [xerr, None, xerr]
        ys = [ydata, eval(dense_curve), eval(fit_curve)]
        yerrs = [yerr, None, yerr]

        capsizes = [kwargs['capsize'], None, kwargs['capsize']]

        fignames = ['_data', '_curve', '_fit_data']

        # I want to get the indices for the selected graphs
        graphs = [graph for graph in range(len(kwargs['graph'])) \
            if kwargs['graph'][graph] == True]
        for i, j in zip(graphs, range(len(graphs))):
        # amazing implementation :)

            if kwargs['split'] == True:
                plt.figure(figsize = kwargs['sizes'][j] if kwargs['sizes'] \
                    != defaults['sizes'] else defaults['sizes'][i])

            plt.errorbar(
                xs[i], ys[i],
                yerr = yerrs[i], xerr = xerrs[i],
                capsize = capsizes[i],
                color = \
                    (color_dict[kwargs['colors'][j]] \
                    if (kwargs['colors'][j] in color_dict.keys() \
                        and type(kwargs['colors']) == list) \
                    else kwargs['colors'][j]) \
                    if kwargs['colors'] != defaults['colors'] \
                    else defaults['colors'][i],
                marker = kwargs['markers'][j] if kwargs['markers'] \
                    != defaults['markers'] else defaults['markers'][i],
                linestyle = kwargs['linestyles'][j] if kwargs['linestyles'] \
                    != defaults['linestyles'] else defaults['linestyles'][i],
                label = r'{}'.format(
                    (kwargs['labels'][j] if (
                        type(kwargs['labels']) == list \
                        and len(kwargs['labels']) == 3 \
                        and kwargs['split'] == True) \
                    else kwargs['labels']) if kwargs['labels'] \
                    != defaults['labels'] else defaults['labels'][i]),
                linewidth = kwargs['linewidth'],
                ecolor = kwargs['ecolor'],
                elinewidth = kwargs['elinewidth'],
                errorevery = kwargs['errorevery'],
                barsabove = kwargs['barsabove'],
                markersize = kwargs['markersize'],
                fillstyle = kwargs['fillstyle'],
                markevery = kwargs['markevery'],
                )

            if type(kwargs['titles'][j]) == str:
                plt.title(r'{}'.format(kwargs['titles'][j] \
                    if kwargs['titles'] != defaults['titles'] \
                    else defaults['titles'][i]))

            if type(kwargs['axis_labels'][0]) == str:
                plt.xlabel(r'{}'.format(kwargs['axis_labels'][0]))
            if type(kwargs['axis_labels'][1]) == str:
                plt.ylabel(r'{}'.format(kwargs['axis_labels'][1]))

            if type(kwargs['legend']) == str:
                plt.legend(loc = kwargs['legend'])
            elif kwargs['legend'] == True:
                plt.legend(loc = 'best')

            if kwargs['save'] != False:
                if type(kwargs['save']) == str:
                    wf = re.search('\.', kwargs['save']).start()
                    # wf, like where_format, where the . is in the savename
                    plt.savefig(
                        kwargs['save'][:wf] + fignames[j] + kwargs['save'][wf:]
                        )
                elif type(kwargs['save']) == list \
                    and len(kwargs['save']) == len(graphs):
                    plt.savefig('{}{{}}'.format(kwargs['save'][j])).format(
                        '.pdf' if '\.' in kwargs['save'][j] else ''
                        )
                else: # maybe redo this
                    if i == 0:
                        plt.savefig('data_scatter.pdf')
                    elif i == 1:
                        plt.savefig('fit_curve.pdf')
                    elif i == 2:
                        plt.savefig('fit_data.pdf')

        plt.show()

    if kwargs['printf']:
        print_func = copy.copy(func)
        for i in range(len(fit_parms)):
            print_func = re.sub( \
                '{{{}}}'.format(parms[i]), str(fit_parms[i]), print_func)
        print(print_func)

    return zip([fit_parms, fit_parms_us])
