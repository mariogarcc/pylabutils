"""
Collection of methods/functions/classes regarding input and output of data.
"""

# standard library imports
import re
import os
import sys
import copy
import codecs
import warnings

import uncertainties as us

from contextlib import contextmanager

# dependency imports
import pandas as pd
import numpy as np

# intra-package imports
##

__all__ = ['wdir', 'read_data', 'tex_table']


@contextmanager
def wdir(path):
    """
    *Yields* a given path as working directory.

    Useful for importing/exporting data that's not locally stored,
    letting you not have to change the working directory back.
    For permanently changing working directory, use os.chdir(<path>)

    >>> with wdir(<path>):
    ...     <do_something>

    > Parameters:

    path : *str*
    Path to desired working directory folder.

    """

    current_dir = os.getcwd()
    os.chdir(path) # change directory
    try:
        yield # in context
    finally: # cleanup
        os.chdir(current_dir) # back to previous directory


###############################################################
"""
===============================================================
"""
###############################################################


def _add_cols(df):
    """
    Function to add new columns to a dataframe based on interactive user input.
    Columns to be added shall be introduced complying with the following regex:

    `r'[\w\.\(\)]+\s*[=,;]\s*<arg>'`

    where arg must be a valid python expression in which references to the
    own dataframe must be keys inside curly brackets: {df_key}

    > Parameters:

    df : *pandas.DataFrame*
    The dataframe the columns will be added to.

    """
    command = input('Add a column:\n')
    if command.lower() in 'no||quit()||exit()||return':
        return

    col_name = command[ \
        re.search(r'[\w\.\(\)]+', command).start(): \
        re.search(r'[\w\.\(\)]+', command).end() \
        ]
    # new column name

    arg = command[re.search(r'[=,;]', command).end():]
    ref_cols = re.findall(r'(?<=\{)\w[\w\.\(\)]*(?=\})', arg)
    # df column names that are referenced to create new columns

    for i in range(len(ref_cols)):
        arg = re.sub(
            '{{{}}}'.format(ref_cols[i]),
            "df['{}']".format(ref_cols[i]),
            arg
            )
    # substituting references

    col_arg = eval(arg)
    df[col_name] = col_arg
    # creating column

    more = input('Would you like to add more columns?\n')
    if more.lower() in 'yes||continue||true':
        return _add_cols(df)
    return



def read_data(filename, **options):
    """
    Reads a table-like file containing data and contains it in a
    `pandas.DataFrame` that behaves like a dictionary.

    > Parameters:

    layout : *str; optional*
    Specified if your data layout follows a vertical or horizontal pattern.
    default : 'vertical'

    delim : *{' ', ',', ', ', '\t', ';'}; optional*
    Specifies which string is to be parsed as delimiter for row values inside
    the data. If `None`, the function calculates it by itself
    default : None

    mod : *bool; optional*
    Specifies whether to add more columns to the dataframe or not.
    default : False

    numeric : *bool; optional*
    Specifies whether the read data should be treated as numeric values.
    default: True

    dtype : *str or dtype or None; optional*
    Optional keyword argument that specifies if all data values can and will
    be read as a specific dtype. It is recommended to leave as `None` unless
    data follows a vertical layout. It is prone to raising exceptions.
    default : None

    astype : *str or dtype or None; optional*
    Same as `dtype` kwarg, but is able to handle exceptions and can be used
    in a horizontal layout.
    default : None

    decimal : *str of length 1; optional*
    Specifies which character should be interpreted as a decimal point
    delimiter.
    default : '.'

    thousands : *str; optional*
    Specifies which string should be interpreted as a thousands separator.
    default : ''

    encoding : *codecs encoding; optional*
    Specifies which encoding `codecs.open()` should use when reading files.
    It is best to leave as default.
    default : 'utf-8'

    engine : *{'python', 'c'}; optional*
    Specifies which engine should be use for parsing. C is faster while Python
    is more feature complete. It is recommended to leave Python.
    default : 'python'

    line_end : *str of length 1; optional*
    Specifies which character the C parser should identify as a line
    terminator.
    default :  None

    excel_engine : *xlrd or None; optional*
    Specifies which engine should be utilized for parsing .xlsx files.
    pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.read_excel.html
    default : None

    squeeze : *bool; optional*
    If the parsed data only contains a column, return a `pandas.Series`.
    default : False

    sheet_name : *str or int or mixed list of str/int or None; optional*
    Specifies which sheets are to be read in a .xlsx file.
    Strings are used for sheet names, integers are used in zero-indexed
    sheet positions.
    Lists of strings/integers are used to request multiple sheets.
    Specify None to get all sheets.
    default : 0

        str|int : DataFrame is returned.
        list|None : Dict of DataFrames is returned, keys representing sheets.

        > Available cases:

        0: 1st sheet as a DataFrame
        1: 2nd sheet as a DataFrame
        “Sheet1_name”: 1st sheet as a DataFrame
        [0,1,”Sheet5_n”]: 1st, 2nd & 5th sheet as a dictionary of DataFrames
        None: All sheets as a dictionary of DataFrames

    cols : *int or list or None; optional*
    Specifies which columns are to be read from the file, in a zero-indexed
    manner.
    default : None

        > Available cases:

        None: parse all columns.
        int: indicates last column to be parsed
        list of ints: indicates list of column numbers to be parsed
        str: indicates comma separated list of Excel column letters and
            column ranges (e.g. “A:E” or “A,C,E:F”). Ranges are inclusive of
            both sides.


    nrows : *int or None; optional*
    Specifies the number of rows to parse
    default : None

    skiprows : *array-like or None; optional*
    Specifies which zero-indexed rows should be ignored.
    default : None

    skipfooter : *int; optional*
    Specifies the amount of rows to be skipped at the bottom of the file.
    Not supported with C engine.
    default : 0

    ints : *bool; optional*
    Specifies if Excel should convert integral floats into int (e.g. 1.0 to 1).
    default : False

    skipinitialspace : *bool; optional*
    Specifies if the parser should skip whitespace after the delimiter
    default : False

    """

    kwargs = dict(
        layout = 'vertical',
        delim = None,
        mod = False,
        numeric = True,
        dtype = None,
        astype = None,
        decimal = '.',
        thousands = '',
        encoding = 'utf-8',
        line_end = None,
        engine = 'python',
        excel_engine = None,
        squeeze = False,
        sheet_name = 0,
        cols = None,
        nrows = None,
        skiprows = None,
        skipfooter = 0,
        ints = False,
        skipinitialspace = False,
    )

    defaults = copy.deepcopy(kwargs)

    kwargs.update(options)

    warnings.filterwarnings('ignore', category = pd.errors.ParserWarning)
    # ignore ParserWarning for engine choice


    # reading file as a dataframe with pandas
    if re.search(r'(\.xlsx)$', filename):
        file_data = pd.read_excel(filename,
            sheet_name = kwargs['sheet_name'],
            usecols = kwargs['cols'],
            dtype = kwargs['dtype'],
            engine = kwargs['excel_engine'],
            nrows = kwargs['nrows'],
            skiprows = kwargs['skiprows'],
            skipfooter = kwargs['skipfooter'],
            thousands = kwargs['thousands'],
            convert_float = kwargs['ints'],
            skipinitialspace = kwargs['skipinitialspace'],
            squeeze = kwargs['squeeze'],
            )

    elif re.search(r'(\.csv)$', filename):
        with codecs.open(filename, 'rU', kwargs['encoding']) as doc:

            temp = pd.read_csv(doc)
            cols = range(len(temp.columns))
            rows = [row for index, row in temp.iterrows()]

        with codecs.open(filename, 'rU', kwargs['encoding']) as doc:
            try:
                file_data = pd.read_csv(doc,
                    sep = kwargs['delim'] if kwargs['delim'] \
                        is not None else( \
                            ', ' if all([', ' in row[col] for row in rows \
                                for col in cols]) \
                        else ('\t' if all(['\t' in row[col] for \
                            row in rows for col in cols]) \
                        else (',' if all([',' in row[col] for \
                            row in rows for col in cols]) \
                            else ' '))),
                    lineterminator = kwargs['line_end'] if kwargs['line_end'] \
                        is not None else( \
                            '\n' if all(['\n' in row[col] for row in rows \
                                for col in cols]) \
                        else ('\r' if all(['\r' in row[col] for \
                            row in rows for col in cols]) \
                        else ('\r\n' if all(['\r\n' in row[col] for \
                            row in rows for col in cols]) \
                            else None))),
                    usecols = kwargs['cols'],
                    dtype = kwargs['dtype'],
                    engine = kwargs['engine'],
                    nrows = kwargs['nrows'],
                    skiprows = kwargs['skiprows'],
                    skipfooter = kwargs['skipfooter'],
                    decimal = kwargs['decimal'],
                    thousands = kwargs['thousands'],
                    skipinitialspace = kwargs['skipinitialspace'],
                    squeeze = kwargs['squeeze'],
                    )

            except ValueError as e:
                if "Unable to convert" in str(e):
                    print("Invalid value encountered in file. Check if there"
                          "are any inf, NaN, or similars in your data.")
                    raise e
                else:
                    raise e
            finally:
                del temp, cols, rows


    elif re.search(r'(\.txt|\.md)$', filename):
        with codecs.open(filename, 'rU', kwargs['encoding']) as doc:

            temp = pd.read_table(doc)#, engine = 'python')
            cols = range(len(temp.columns))
            rows = [row for index, row in temp.iterrows()]
        # have to open again, otherwise throws EmptyDataError, don't know why
        with codecs.open(filename, 'rU', kwargs['encoding']) as doc:
            try:
                file_data = pd.read_table(doc,
                    sep = kwargs['delim'] if kwargs['delim'] \
                        is not None else( \
                            ', ' if all([', ' in row[col] for row in rows \
                                for col in cols]) \
                        else ('\t' if all(['\t' in row[col] for \
                            row in rows for col in cols]) \
                        else (',' if all([',' in row[col] for \
                            row in rows for col in cols]) \
                            else ' '))),
                    lineterminator = kwargs['line_end'] if kwargs['line_end'] \
                        is not None else( \
                            '\n' if all(['\n' in row[col] for row in rows \
                                for col in cols]) \
                        else ('\r' if all(['\r' in row[col] for \
                            row in rows for col in cols]) \
                        else ('\r\n' if all(['\r\n' in row[col] for \
                            row in rows for col in cols]) \
                            else None))),
                    usecols = kwargs['cols'],
                    dtype = kwargs['dtype'],
                    engine = kwargs['engine'],
                    nrows = kwargs['nrows'],
                    skiprows = kwargs['skiprows'],
                    skipfooter = kwargs['skipfooter'],
                    decimal = kwargs['decimal'],
                    thousands = kwargs['thousands'],
                    skipinitialspace = kwargs['skipinitialspace'],
                    squeeze = kwargs['squeeze'],
                    )

            except ValueError as e:
                if "Unable to convert" in str(e):
                    print("Invalid value encountered in file. Check if there"
                          "are any inf, NaN, or similars in your data.")
                    raise e
                else:
                    raise e
            finally:
                del temp, cols, rows

    else:
        raise TypeError('file type readability not yet implemented.')

    global _file_data
    _file_data = copy.deepcopy(file_data)

    # second part of criteria for reading files: allow horizontality
    temp = file_data


    # default layout is vertical||columsn which requires no action
    if kwargs['layout'] in 'horizontal||rows':
        lead_key = file_data.keys()[0]
        temp = file_data.set_index(lead_key).T.rename_axis(lead_key) \
            .rename_axis(None, 1).reset_index()

        del lead_key

    if kwargs['numeric']:
        temp = temp.apply(pd.to_numeric, errors = 'coerce')

    if kwargs['astype']:
        temp = temp.astype(kwargs['astype'])

    data = copy.deepcopy(temp)
    del temp


    if kwargs['mod']:
        _add_cols(data)


    global _data
    _data = copy.deepcopy(data)

    return data

# To do:
# add uncertainty support and extensive data reading.
# group csv and table contexts.


###############################################################
"""
===============================================================
"""
###############################################################


# No imports required

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


def tex_table(data, data_titles, **options):
    """
    Generates a simple Latex table containing numeric data.

    > Parameters:

    data : *N x array-like*
    Data that will be presented in the table.

    data_titles : *N x str, array-like*
    Titles for the given data.

    prec : *int or N x int, array-like; optional*
    Specifies the amount of decimal digits to show on a decimal representation
    of a number. Can be set to a list of values corresponding to one value for
    each data list. If set to a single value, it will apply that value to
    all lists of data.
    Negative values can be used to round integers.
    default : 2 for every list that has a decimal point, 0 otherwise

    shape : *str; optional*
    Chooses whether the table should be of vertical or horizontal layout.
    default: 'vertical'

    sep : *str; optional*
    Specifies which kind of separation lines between elements are to be had
    inside the table.
    default : 'horizontal'

    fit : *str; optional*
    Specifies which style of text fit should be applied to the table.
    default : 'H'

    caption : *bool, None or str; optional*
    Chooses whether to print the "\caption" command inside the table. Can be
    provided with a string argument to put inside the command.
    default : None

    label : *bool, None or str; optional*
    Chooses whether to print the "\label" command inside the table. Can be
    provided with a string argument to put inside the command.
    default : None

    exp : *bool or N x bool, array-like; optional*
    Chooses whether to use power-of-ten (scientific) notation in the numbers
    representation for any of the data lists.
    default : False

    exp_prec : *int or N x int, array-like; optional*
    Specifies the amount of decimal digits to show on a power-of-ten
    (scientific) representation of a number. Can be set to a list of values
    corresponding to one value for each data list. If set to a single value,
    it will apply that value to all lists of data.
    Can only take values greater than or equal to 0.
    default : 2

    fwf : *bool; optional*
    Chooses whether to use fixed width formatting for representing non-negative
    numbers. This means a space will be added before positive numbers in their
    representation, to account for the missing negative sign `-`.
    default : False

    font_size_type : *str or None; optional*
    Changes font size inside table.
    default : None

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
                raise ValueError("'{}' is not a valid value for '{}'" \
                    .format(kwargs[option], option))
                return

    else:
        if len(data) == 1:
            data = data[0]

        if len(data) != len(kwargs['prec']) or len(data) != len(data_titles):
            raise ValueError("data's, data titles' and" \
                " precisions' sizes don't match")
            return
        else:
            for i in range(len(data)):
                if len(data[i]) != len(data[i-1]):
                    raise ValueError("data items' sizes don't match")
                    return

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

    return print(table)

# should I make formatting have space for positive numbers or remove it?
# > added kwarg to choose
# should I add an extra space on row start and end? there is a space
# after and before & signs, so I should probably do that > done


###############################################################
"""
===============================================================
"""
###############################################################


def _print_measure(val, unc, fmt = None, name = None):
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

    name_str = "{{name}} = " if name is not None else ""

    return print("{{name_str}}{{measure:{fmt}}}" \
        .format(fmt = fmt) \
        .format(name_str = name_str, measure = measure) \
        )
