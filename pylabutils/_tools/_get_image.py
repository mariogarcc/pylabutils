import re

__all__ = ['_get_image']

# note that this works only with 'x' as the independent variable
# returns callable, for static typing
def _get_image(x, *values, func_str = None, parms = None,
    scope = (globals(), locals())):
    """
    Gets the image of a string function that complies with the criteria stated
    in the `fit` method.
    """
    if not func_str:
        raise ValueError("missing essential kwarg `func_str`")

    # parms is a list with the string names for all parameters
    if not parms:
        parms = re.findall(r'(?<=\{)\w[\w\.\(\)]*(?=\})', func_str)
        # finds parameter names

        for parm in parms:
            if parms.count(parm) > 1:
                temp = parms[::-1]
                temp.remove(parm)
                parms = temp[::-1].copy()
        # removes all duplicates from the end back
    # this is already in the main fit method. Should I remove it?
    # to also work as an independent tool it would need _ffixx...

    # substituting the parameters indicated in the function for their values
    for i in range(len(parms)):
        func_str = re.sub( \
            f'{{{parms[i]}}}', str(values[i]), func_str)

    scope[0].update(globals())
    scope[1].update(locals())

    if '=' in func_str:
        image = eval(func_str[func_str.find('=')+1:], scope[0], scope[1])
    else:
        image = eval(func_str, scope[0], scope[1])

    return image
