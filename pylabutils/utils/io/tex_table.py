__all__ = ['tex_table']


_tex_table_values = dict(
    shape = ('v', 'h', 'ver', 'hor', 'vertical', 'horizontal'),
    sep = ('v', 'h', 'f', 'no', 'ver', 'hor', # 'n' is also in 'horizontal'
        'vertical', 'horizontal', 'full', 'none'
        ),
    fit = ('h', 'h!', 'b', 't', 'H'),
    loc = ('c', 'l', 'r', 'center', 'left', 'right',
        'centering', 'raggedleft', 'raggedright'
        ),
    font_size_type = (
        'Huge', 'huge', 'LARGE', 'Large',
        'normalsize', 'small', 'footnotesize',
        'scriptsize', 'tiny', None,
        ),
    )


def tex_table(data, data_titles, **options) -> str:
    """
    Generates a simple Latex table containing numeric data.


    \> Parameters:

    `data` : *N x array-like*

    Data that will be presented in the table.


    `data_titles` : *N x str, array-like*

    Titles for the given data.


    `prec` : *int or N x int, array-like; optional*

    Specifies the amount of decimal digits to show on a decimal representation
    of a number. Can be set to a list of values corresponding to one value for
    each data list. If set to a single value, it will apply that value to
    all lists of data.
    Negative values can be used to round integers.

    default : `2` for every list that has a decimal point, `0` otherwise
    (will be revised for better functioning)


    `shape` : *str; optional*

    Chooses whether the table should be of vertical or horizontal layout.

    default: `'vertical'`

    `sep` : *str; optional*

    Specifies which kind of separation lines between elements are to be had
    inside the table.

    default : `'horizontal'`


    `fit` : *str; optional*

    Specifies which style of text fit should be applied to the table.

    default : `'H'`


    `caption` : *bool, None or str; optional*

    Chooses whether to print the `\caption` command inside the table. Can be
    provided with a string argument to put inside the command.

    default : `None`


    `label` : *bool, None or str; optional*
    Chooses whether to print the `\label` command inside the table. Can be
    provided with a string argument to put inside the command.

    default : `None`


    `exp` : *bool or N x bool, array-like; optional*

    Chooses whether to use power-of-ten (scientific) notation in the numbers
    representation for any of the data lists.

    default : `False`


    `exp_prec` : *int or N x int, array-like; optional*

    Specifies the amount of decimal digits to show on a power-of-ten
    (scientific) representation of a number. Can be set to a list of values
    corresponding to one value for each data list. If set to a single value,
    it will apply that value to all lists of data.
    Can only take values greater than or equal to 0.

    default : `2`

    `fwf` : *bool; optional*

    Chooses whether to use fixed width formatting for representing non-negative
    numbers. This means a space will be added before positive numbers in their
    representation, to account for the missing negative sign `-`. Will consider
    adding the option to show a `+` sign in the future as well.

    default : `False`


    `font_size_type` : *str or None; optional*

    Changes font size inside table.

    default : `None`


    \> Returns:

    The string containing the TeX table.

    """


    kwargs = dict(
        prec = [2 if any(['.' in str(num) for num in data_list]) \
            else 0 for data_list in data],
        shape = 'vertical',
        sep = 'horizontal',
        loc = 'centering',
        fit = 'H',
        caption = None,
        label = None,
        exp = False,
        exp_prec = 2,
        fwf = False, # formatting with whitespace for non negative numbers
        font_size_type = None,
    )

    options.update({k: v.lower() for k, v in
        [(k, v) for k, v in options.items()][:4] if type(v) == str})
    # maybe beautifyable, but gets job done. gives freedom at naming kwargs

    kwargs.update(options)

    if any([kwargs[option] not in _tex_table_values[option] \
            for option in _tex_table_values.keys()]): # fast check
        for option in _tex_table_values.keys():
            if kwargs[option] not in _tex_table_values[option]:
                raise ValueError("'{!r}' is not a valid value for '{!s}'" \
                    .format(kwargs[option], option))

    else:
        if len(data) == 1:
            data = data[0]

        if len(data) != len(kwargs['prec']) or len(data) != len(data_titles):
            raise ValueError("data's, data titles' and" \
                " precisions' sizes don't match")
            # allow using a single precision value for everything later
        else:
            for i in range(len(data)):
                if len(data[i]) != len(data[i-1]):
                    raise ValueError("data items' sizes don't match")

    # argument validation

    head  = '' \
        + '\\begin{{table}}[{}]\n'.format(kwargs['fit']) \
        + '\\{}\n'.format(kwargs['font_size_type']) \
            * (kwargs['font_size_type'] is not None) \
        + '\\{}\n'.format(kwargs['loc']) \
        + '\\begin{tabular}'
        # obligatory

    prec = kwargs['prec']
    exp_prec = kwargs['exp_prec']
    exp = kwargs['exp']

    if kwargs['shape'] in 'vertical':

        disp = '' \
            + '{' \
            + ('|' * (kwargs['sep'] in ('vertical''||''full')) + 'c') \
            * len(data) \
            + '|' * (kwargs['sep'] in ('vertical''||''full')) \
            + '}'


        titles = '' \
            + '\n' \
            + '\\hline\n' * (kwargs['sep'] in ('horizontal''||''full')) \
            + ' '

        for i in range(len(data_titles)):
            titles += data_titles[i]
            if i != len(data_titles) - 1:
                titles += ' & '
            else:
                titles += ' ' \
                    + '\\''\\''\n' \
                    + '\\hline\n'

        rows = ''
        for i in range(len(data[0])):
            row = ' '
            for j in range(len(data)):

                precision = \
                    prec[j] if (type(prec) == list \
                        and len(prec) != 1) \
                    else (prec if type(prec) == int \
                        else prec[0]) # list format or single value

                if kwargs['exp']:
                    exp = kwargs['exp']
                    exp_val = \
                        exp[j] if (type(exp) == list \
                            and len(exp) != 1) \
                        else (exp if type(exp) == bool \
                            else exp[0]) # list format or single value
                    exp_precision = \
                        exp_prec[j] if (type(exp_prec) == list \
                            and len(exp_prec) != 1) \
                        else (exp_prec if type(exp_prec) == int \
                            else exp_prec[0]) # list format or single value
                else:
                    exp_val = False # bit ugly, this is

                num = round(data[j][i], precision)

                formatting = ':{}.{}{}'.format( \
                    ' ' if kwargs['fwf'] else '',
                    '0' if (precision <= 0 and exp_val == False) \
                        else (precision if exp_val == False \
                            else exp_precision),
                    'e' if exp_val == True else 'f'
                    )

                row += '{{{}}}'.format(formatting).format(num)

                if j != len(data)-1:
                    row += ' & '

            row += ' ''\\''\\''\n'

            if i != len(data[0])-1:
                row += \
                    ' \\hline\n' * (kwargs['sep'] in ('horizontal''||''full'))

            rows += row

        body = disp + titles + rows


    elif kwargs['shape'] in 'horizontal':

        disp = '' \
            + '{' \
            + '|' * (kwargs['sep'] in ('vertical''||''full')) \
            + 'c|' \
            + ('c' + '|' * (kwargs['sep'] in ('vertical''||''full'))) \
            * len(data) \
            + '}'

        rows = '' \
            + '\n' \
            + '\\hline\n' * (kwargs['sep'] in ('horizontal''||''full'))

        for i in range(len(data)):
            row = ' ' + data_titles[i] + ' & '
            for j in range(len(data[0])):

                precision = \
                    prec[i] if (type(prec) == list \
                        and len(prec) != 1) \
                    else (prec if type(prec) == int \
                        else prec[0]) # list format or single value

                if kwargs['exp']:
                    exp = kwargs['exp']
                    exp_val = \
                        exp[i] if (type(exp) == list \
                            and len(exp) != 1) \
                        else (exp if type(exp) == bool \
                            else exp[0]) # list format or single value
                    exp_precision = \
                        exp_prec[i] if (type(exp_prec) == list \
                            and len(exp_prec) != 1) \
                        else (exp_prec if type(exp_prec) == int \
                            else exp_prec[0]) # list format or single value
                else:
                    exp_val = False

                num = round(data[i][j], precision)

                formatting = ':{}.{}{}'.format( \
                    ' ' if kwargs['fwf'] else '',
                    '0' if (precision <= 0 and exp_val == False) \
                        else (precision if exp_val == False \
                            else exp_precision),
                    'e' if exp_val == True else 'f'
                    )

                row += '{{{}}}'.format(formatting).format(num) # add num

                if j != len(data[0])-1:
                    row += ' & '

            row += ' ''\\''\\''\n' \

            if i != len(data)-1:
                row += \
                    ' \\hline\n' * (kwargs['sep'] in ('horizontal''||''full'))
            # complete row

            rows += row # add row

        body = disp + rows

    tail = '' \
        + '\\hline\n' * (kwargs['sep'] in ('horizontal''||''full')) \
        + '\\end{tabular}\n' \
        + '\\caption{{{}}}\n'.format( \
            (str(kwargs['caption']) * (type(kwargs['caption']) == str))) \
            * (kwargs['caption'] != False) \
        + '\\label{{{}}}\n'.format( \
            (str(kwargs['label']) * (type(kwargs['label']) == str))) \
            * (kwargs['label'] != False) \
        + '\\end{table}\n'

    table = head + body + tail

    return table

