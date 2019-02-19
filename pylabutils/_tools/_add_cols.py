import re
import pandas

def _add_cols(df: pandas.DataFrame, scope = None) -> None:
    """
    A function to add new columns to a dataframe based on interactive user
    input.
    Columns to be added shall be introduced complying with the following
    regex:

    `r'[\w\.\(\)]+\s*[=,;]\s*<arg>'`

    where `<arg>` must be a valid python expression in which references to the
    own dataframe must be keys inside curly brackets: `{df_key}`


    \> Parameters:

    `df` : *pandas.DataFrame*

    The dataframe the columns will be added to.


    \> Returns:

    `None`, because its point is to modify the existent database.

    """
    command : str = input("\nAdd a column:\n")
    if command.lower() in ['n', 'no', 'quit()', 'exit', 'return']:
        return

    col_name : str = command[ \
        re.search(r'[\w\.\(\)]+', command).start(): \
        re.search(r'[\w\.\(\)]+', command).end() \
        ]
    # new column's name

    arg : str = command[re.search(r'[=,;]', command).end():]
    # the new column's "function"
    ref_cols = re.findall(r'(?<=\{)\w[\w\.\(\)]*(?=\})', arg)
    # df column names that are referenced to create new columns

    for i in range(len(ref_cols)):
        arg = re.sub(
            '{{{}}}'.format(ref_cols[i]),
            'df[\'{}\']'.format(ref_cols[i]),
            arg
            )
    # substituting references

    if scope is not None:
        scope[0].update(globals())
        scope[1].update(locals())

    col_arg = eval(arg, scope[0], scope[1])
    # pandas.Series for type checking
    df[col_name] = col_arg
    # creating column

    more : str = input("\nWould you like to add more columns?\n")
    if more.lower() in ['y', 'yes', 'continue', 'true']:
        return _add_cols(df)
    return

