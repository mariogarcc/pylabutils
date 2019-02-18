import uncertainties as us

__all__ = ['_print_measure']

def _print_measure(val, unc, fmt = None, name = None):
    """
    Prints a pair of values (value, uncertainty) using the `uncertainties`
    module formatting via kwarg `fmt`.
    """
    if fmt is None:
        # d, f or e formatting? depends on size
        nfmt = \
            'e' if ((unc >= 1000 or unc <= 0.001) and \
                (val >= unc or val <= 0.001) or \
                val >= 1000) else \
            'd' if (unc >= 10 and val >= unc) else \
            'f'

        fmt = '.2uL'
        fmt = fmt[:-1] + nfmt + fmt[-1]

    measure = us.ufloat(val, unc)

    name_str = "{name} = ".format(name = name) if name is not None else ""

    print("{{name_str}}{{measure:{fmt}}}" \
        .format(fmt = fmt) \
        .format(name_str = name_str, measure = measure) \
        )
    return None
