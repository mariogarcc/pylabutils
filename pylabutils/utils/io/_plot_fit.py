import re
import copy

import numpy as np
import matplotlib.pyplot as plt

from ..._tools._colors import color_dict


__all__ = ['_plot_fit']



def _plot_fit(xdata, ydata, scope = (globals(), locals()), **options):
    """
    Plots for fit functions.
    """

    kw = dict(
        func_str = None, # additional kwarg, does not appear in fit()
        # add _func_image option instead of specifying func by str
        yerr = None,
        xerr = None,
        absolute_err = True, # need to add this in plotting
        graph = [True, True, False],
        errorbars = True,
        sizes = [(6, 4), (6, 4), (6, 4)],
        xlim = None,
        ylim = None,
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
    ) # default kwargs values

    defaults = copy.deepcopy(kw)
    kw.update(options)

    if type(kw['func_str']) != str:
        raise ValueError("missing essential keyword argument `func_str`")

    if kw['graph'] == True:
        kw['graph'] = [True, True, False]

    if not kw['graph'] or not any(kw['graph']):
        return None

    xloc = re.search(r'(?<=[\s\*\+\/\%\(])x(?=[\s\*\+\/\%\)])',
        ' '+kw['func_str']+' ').start()-1
    tempf = [kw['func_str'][i] if i != xloc else 'xdata' \
        for i in range(len(kw['func_str']))]
    kw['func_str'] = copy.deepcopy(''.join(tempf))

    # graph plots
    xdata = np.array(xdata)
    xvals = np.linspace( \
        float(min(xdata)), float(max(xdata)), kw['linspace_vals'])

    if kw['errorbars']:
        yerr = np.array(kw['yerr']) if kw['yerr'] \
            is not None else None
        xerr = np.array(kw['xerr']) if kw['xerr'] \
            is not None else None

    dense_curve = re.sub('xdata', 'xvals', kw['func_str'])

    scope[0].update(globals())
    scope[1].update(locals())

    xs = [xdata, xvals, xdata]
    xerrs = [xerr, None, xerr]
    ys = [
          ydata,
          eval(dense_curve, scope[0], scope[1]),
          eval(kw['func_str'], scope[0], scope[1])
         ]
    yerrs = [yerr, None, yerr]

    capsizes = [kw['capsize'], None, kw['capsize']]

    fignames = ['_data', '_curve', '_fit_data']

    # I want to get the indices for the selected graphs
    graphs = [graph for graph in range(len(kw['graph'])) \
        if kw['graph'][graph] == True]
    for i, j in enumerate(graphs):
    # amazing implementation :)

        if kw['split'] == True:
            plt.figure(figsize = kw['sizes'][i] if kw['sizes'] \
                != defaults['sizes'] else defaults['sizes'][j])

        plt.errorbar(
            xs[j], ys[j],
            yerr = yerrs[j], xerr = xerrs[j],
            capsize = capsizes[j],
            color = \
                (color_dict[kw['colors'][i]] \
                if kw['colors'][i] in color_dict.keys() \
                else kw['colors'][i]) \
                if kw['colors'] != defaults['colors'] \
                else defaults['colors'][j],
            marker = kw['markers'][i] if kw['markers'] \
                != defaults['markers'] else defaults['markers'][j],
            linestyle = kw['linestyles'][i] if kw['linestyles'] \
                != defaults['linestyles'] else defaults['linestyles'][j],
            label = r'{}'.format(
                (kw['labels'][i] if (
                    type(kw['labels']) == list \
                    and len(kw['labels']) == 3 \
                    and kw['split'] == True) \
                else kw['labels']) if kw['labels'] \
                != defaults['labels'] else defaults['labels'][j]),
            linewidth = kw['linewidth'],
            ecolor = kw['ecolor'],
            elinewidth = kw['elinewidth'],
            errorevery = kw['errorevery'],
            barsabove = kw['barsabove'],
            markersize = kw['markersize'],
            fillstyle = kw['fillstyle'],
            markevery = kw['markevery'],
            )
            # **kwargs, but careful not to override things

        if kw['xlim']:
            plt.xlim(kw['xlim'])
        if kw['ylim']:
            plt.ylim(kw['ylim'])

        if type(kw['titles']) == str:
            plt.title(r'{}'.format(kw['titles']))
        elif type(kw['titles']) == list \
                and type(kw['titles'][i]) == str:
            plt.title(r'{}'.format(kw['titles'][i] \
                if kw['titles'] != defaults['titles'] \
                else defaults['titles'][j]))

        if type(kw['axis_labels'][0]) == str:
            plt.xlabel(r'{}'.format(kw['axis_labels'][0]))
        if type(kw['axis_labels'][1]) == str:
            plt.ylabel(r'{}'.format(kw['axis_labels'][1]))

        if type(kw['legend']) == str:
            plt.legend(loc = kw['legend'])
        elif kw['legend'] == True:
            plt.legend(loc = 'best')

        if type(kw['save']) == str or kw['save'] == True:
            # this works bad, redo
            if kw['split'] == False and type(kw['save']) == str:
                plt.savefig(kw['save'] + '{}'.format(
                    '.pdf' if '.' not in kw['save'] else ''))

            elif kw['split'] == False and kw['save'] == True:
                plt.savefig('figure.pdf')

            else:
                if type(kw['save']) == str:
                    if '.' in kw['save']:
                        wf = re.search(r'\.', kw['save']).start()
                        # wf, like where_format, where the . is in the savename
                        plt.savefig(
                            kw['save'][:wf] + fignames[i] + kw['save'][wf:])
                    else:
                        plt.savefig(kw['save'] + fignames[i] + '.pdf')

                elif type(kw['save']) == list \
                    and len(kw['save']) == len(graphs):
                    plt.savefig('{}{{}}'.format(kw['save'][i])).format(
                        '.pdf' if '.' not in kw['save'][i] else '')

                else:
                    if i == 0:
                        plt.savefig('data_scatter.pdf')
                    elif i == 1:
                        plt.savefig('fit_curve.pdf')
                    elif i == 2:
                        plt.savefig('fit_data.pdf')

    plt.show()
    return