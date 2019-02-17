import re

def _ffixx(func_str : str, custom_x : str) -> str:
    """
    Finds and replaces a custom named independent variable in a function string
    for the standard 'x', returning the new string.
    """
    # identifying the independent variable in the function string
    x_str = custom_x if type(custom_x) == str else 'x'

    custom_x = re.search(r'(?<=\[)\w[\w\.\(\)]*(?=\])', func_str)
    # square brackets notation overrides custom_x

    if custom_x:
        x_str = func_str[custom_x.start():custom_x.end()]
    # changing it for 'x'
    return re.sub(r'\[{}\]'.format(x_str), 'x', func_str)
