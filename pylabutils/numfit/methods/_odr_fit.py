import scipy.odr as sodr

def _odr_fit(_func_image, xdata, ydata, **options):
    """
    Computes an ODR fit using scipy.ODR.ODR based on a _func_image format.
    """

    kw = dict(
        beta0 = None,
        xerr = None,
        yerr = None,
        jfit_type = None,
        jderiv = None,
        jvar_calc = None,
        jdel_init = None,
        jrestart = None,
    )

    kw.update(options)

    data = sodr.RealData(xdata, ydata, sx = kw['xerr'], sy = kw['yerr'])

    def _mod_func(parms, x):
        return _func_image(x, *parms)
    # model takes arguments swapped...

    model = sodr.Model(_mod_func)

    odr = sodr.ODR(data, model, beta0 = kw['beta0'])
    odr.set_job(
        fit_type = kw['jfit_type'],
        deriv = kw['jderiv'],
        var_calc = kw['jvar_calc'],
        del_init = kw['jdel_init'],
        restart = kw['jrestart'],
    )

    output = odr.run()

    return output.beta, output.sd_beta