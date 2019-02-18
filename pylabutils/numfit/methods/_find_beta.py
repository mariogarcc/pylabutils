import numpy as np

__all__ = ['_find_beta']

def _find_beta(func, xdata, ydata, min_func, nparms, **options):
    """
    Finds optimal initial values for the parameters for a function to be
    fit by some numerical method.
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
            xy_max, xy_min = max(x_max, y_max), min(x_min, y_min)
            if kw['bounds'] == None or kw['bounds'] == (-np.inf, np.inf):
                kw['bounds'] = [
                    [-max(abs(xy_max), abs(xy_min)),
                      max(abs(xy_max), abs(xy_min)),]
                    ] * nparms
            elif len(kw['bounds']) == 2 \
                    and type(kw['bounds'] not in (list, tuple, np.ndarray)):
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
            # you can introduce all kwargs in one go using comprehension
            # with keys, values removing 'de_' ([3:])
        except:
            raise ValueError("couldn't find beta")

        return result.x

    else:
        print("{!r} is not implemented yet".format(kw['fb_method']))
        return

    return

