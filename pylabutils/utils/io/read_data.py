import re
import copy
import codecs
import warnings

import pandas as pd

from ..._tools._add_cols import _add_cols

__all__ = ['read_data']



def read_data(filename, **options):
    """
    Reads a table-like file containing data and contains it in a
    `pandas.DataFrame` that behaves like a dictionary.


    \> Parameters:

    `layout` : *str; optional*
    Specified if your data layout follows a vertical or horizontal pattern.

    default : `'vertical'`


    `delim` : *`{' ', ',', ', ', '\t', ';'}`; optional*

    Specifies which string is to be parsed as delimiter for row values inside
    the data. If `None`, the function calculates it by itself

    default : `None`


    `mod` : *bool; optional*

    Specifies whether to add more columns to the dataframe or not.

    default : `False`


    `numeric` : *bool; optional*

    Specifies whether the read data should be treated as numeric values.

    default: True


    `dtype` : *str or dtype or None; optional*

    Optional keyword argument that specifies if all data values can and will
    be read as a specific dtype. It is recommended to leave as `None` unless
    data follows a vertical layout. It is prone to raising exceptions.

    default : `None`


    `astype` : *str or dtype or None; optional*

    Same as `dtype` kwarg, but is able to handle exceptions and can be used
    in a horizontal layout.

    default : `None`


    `dropna` : *bool; optional*

    Removes columns with all N/A values.

    default : `True`


    `decimal` : *str of length 1; optional*

    Specifies which character should be interpreted as a decimal point
    delimiter.

    default : `'.'`


    `thousands` : *str; optional*

    Specifies which string should be interpreted as a thousands separator.

    default : `''`


    `encoding` : *codecs encoding; optional*

    Specifies which encoding `codecs.open()` should use when reading files.
    It is best to leave as default.

    default : `'utf-8'`


    `engine` : *`{'python', 'c'}`; optional*

    Specifies which engine should be use for parsing. C is faster while Python
    is more feature complete. It is recommended to leave Python.

    default : `'python'`


    `line_end` : *str of length 1; optional*

    Specifies which character the C parser should identify as a line
    terminator.

    default : `None`


    `excel_engine` : *xlrd or None; optional*

    Specifies which engine should be utilized for parsing .xlsx files.
    pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.read_excel.html

    default : `None`


    `squeeze` : *bool; optional*

    If the parsed data only contains a column, return a `pandas.Series`.

    default : `False`


    `sheet_name` : *str or int or mixed list of str/int or None; optional*

    Specifies which sheets are to be read in a .xlsx file.
    Strings are used for sheet names, integers are used in zero-indexed
    sheet positions.
    Lists of strings/integers are used to request multiple sheets.
    Specify None to get all sheets.

    default : `0`

        str|int : DataFrame is returned.
        list|None : `dict` of DataFrames is returned, keys representing sheets.

        \> Available cases:

        0: 1st sheet as a DataFrame
        1: 2nd sheet as a DataFrame
        "Sheet1_name": 1st sheet as a DataFrame
        [0, 1, "Sheet5_n"]: 1st, 2nd and 5th sheet as a `dict` of DataFrames
        None: All sheets as a `dict` of DataFrames



    `cols` : *int or list or None; optional*

    Specifies which columns are to be read from the file, in a zero-indexed
    manner.

    default : `None`

        \> Available cases:

        None: parse all columns.
        int: indicates last column to be parsed
        list of ints: indicates list of column numbers to be parsed
        str: indicates comma separated list of Excel column letters and
            column ranges (e.g. "A:E" or "A,C,E:F"). Ranges are inclusive of
            both sides.



    `nrows` : *int or None; optional*

    Specifies the number of rows to parse

    default : `None`


    `skiprows` : *array-like or None; optional*

    Specifies which zero-indexed rows should be ignored.

    default : `None`


    `skipfooter` : *int; optional*

    Specifies the amount of rows to be skipped at the bottom of the file.
    Not supported with C engine.

    default : `0`


    `ints` : *bool; optional*

    Specifies if Excel should convert integral floats into int (e.g. 1.0 to 1).

    default : `False`


    `skipinitialspace` : *bool; optional*

    Specifies if the parser should skip whitespace after the delimiter

    default : `False`


    \> Returns:

    The pandas.DataFrame containing the data.

    """

    kwargs = dict(
        layout = 'vertical',
        delim = None,
        mod = False,
        numeric = True,
        dtype = None,
        astype = None,
        dropna = True,
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
                          " are any inf, NaN, or similars in your data."
                          " Columns longer than others can also be a problem.")
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
                          " are any inf, NaN, or similars in your data.")
                    raise e
                else:
                    raise e
            finally:
                del temp, cols, rows

    else:
        raise TypeError("file type readability not yet implemented.")

    # second part of criteria for reading files: allow horizontality
    temp = copy.deepcopy(file_data)

    # default layout is vertical||columns which requires no action
    if kwargs['layout'] in "horizontal||rows":
        lead_key = file_data.keys()[0]
        temp = file_data \
                .set_index(lead_key) \
                .T.rename_axis(lead_key) \
                .rename_axis(None, 1) \
                .reset_index()

        del lead_key

    if kwargs['numeric']:
        temp = temp.apply(pd.to_numeric, errors = 'coerce')

    if kwargs['astype']:
        temp = temp.astype(kwargs['astype'])

    if kwargs['dropna']:
        temp = temp.dropna(axis = 1, how = 'all')


    data = copy.deepcopy(temp)
    del temp


    if kwargs['mod']:
        _add_cols(data)

    return data

# To do:
# add uncertainty support and extensive data reading.
# group csv and table contexts.