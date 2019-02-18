import copy

import numpy as np


__all__ = ['multisort']



def multisort(guide, *data, **options):
    """
    Sorts a `guide` via criterion and then applies the same index displacement
    to all other items in `data`.


    \> Parameters:

    `guide` : *array-like*

    The item the method will be based on to sort the additional items.


    `data` : *N x array-like*

    The list of items that will be sorted according to the result from the
    `guide` sort.


    `criterion` : *str; optional*

    Method for sorting the `guide`.

    default : `'asc'`


    `inplace` : *bool; optional*

    Chooses whether to sort the items in-place.

    default : `False`


    `include_guide` : *bool; optional*

    If `inplace == False`, chooses whether to include `guide` into the
    returned object from the function call.

    default : `True`


    \> Returns:

    The sorted data in order of input, varying depending on if you chose
    to do an in-place sort, to include the guide, etc.

    """

    from .._tools._ms_methods import \
        _ms_asc_ind, \
        _ms_desc_ind, \
        _ms_dalt_ind, \
        ms_method_names

    kwargs = dict(
        criterion = 'asc',
        inplace = False,
        include_guide = True,
        showres = False,
    )

    kwargs.update(options)

    for value in kwargs.keys():
        if value in options.keys() and type(kwargs[value]) \
                != type(options[value]):
            # quick check for kwarg validness
            raise TypeError("{!r} is an invalid value for `{!s}`"
                .format(options[value], value))

    try:
        method = eval([name for name in ms_method_names \
            if kwargs['criterion'] in name][0])
            # similar to re.groups()
    except:
        print("specified criterion is invalid; default set to asc")
        method = _ms_asc_ind

    sorting_indices = method(guide)
    if kwargs['showres']:
        print(("Resulting indices after sorting: {}").format(sorting_indices))

    if len(data) == 1 and type(data[0][0]) in (list, tuple, np.ndarray):
        data = data[0]
    # allows data to be introduced separately or clustered

    if kwargs['inplace']:

        for data_list in data:
            temp_list = copy.copy(data_list)
            for index in range(len(data_list)):
                data_list[index] = temp_list[sorting_indices[index]]

        if kwargs['include_guide']:
            temp_guide = copy.copy(guide)
            for index in range(len(guide)):
                guide[index] = temp_guide[sorting_indices[index]]

        return None

    sorted_data = [[data_list[new_index] for new_index in sorting_indices] \
        for data_list in data]

    if kwargs['include_guide']:
        sorted_guide = [guide[new_index] for new_index in sorting_indices]
        sorted_data.insert(0, sorted_guide)

    return sorted_data

# try implementing yield, with, contextmanager, for result returning
#   to avoid use of temp items
