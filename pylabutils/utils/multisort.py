import copy
import numpy as np

__all__ = ['multisort', 'ms_methods']

def _ms_asc_ind(item):
    """
    Sorts elements in ascending order and returns a list of their previous
    indices compared to their current ones.

    > Parameters:

    item : *array-like*
    """
    if type(item) in [list, tuple]:
        myitem = [[x, item.index(x)] for x in item]
        myitem.sort() # sorts based on the first value for each pair
        return [element[1] for element in myitem] # indices

    elif type(item) == np.ndarray:
        return list(np.argsort(item)) # literally returns sorting indices

    else:
        return 'Item type not recognized'


def _ms_desc_ind(item):
    """
    Sorts elements in descending order and returns a list of their previous
    indices compared to their current ones.

    > Parameters:

    item : *array-like*
    """
    if type(item) in [list, tuple]:
        myitem = [[x, item.index(x)] for x in item]
        myitem.sort(reverse = True)
        return [element[1] for element in myitem]

    elif type(item) == np.ndarray:
        return list(np.argsort(item))[::-1]

    else:
        return 'Item type not recognized'


def _ms_dalt_ind(item):
    """
    Sorts elements in a sign-alternating descending order and returns a list
    of their previous indices compared to their current ones.

    > Parameters:

    item : *array-like*
    """
    if type(item) == np.ndarray:
        raise TypeError('numpy.ndarray not yet supported for this sort')

    temp = [[x, item.index(x)] for x in item]
    myitem = []
    while temp: # checks if temp is not empty in a fancy manner
        # max value iteration
        try:
            myitem.append(temp[temp.index(max(temp))])
            del temp[temp.index(max(temp))]
        except(Exception):
            print('Some error occurred')
            pass
        # min value iteration
        try:
            myitem.append(temp[temp.index(min(temp))])
            del temp[temp.index(min(temp))]
        except(Exception):
            print('Some error occurred')
            pass
        # could also be done by comparisons, by measuring maximum and minimum
        # distance between elements
    return [element[1] for element in myitem]


ms_method_names, ms_methods = \
    zip(*[[name, func] for (name, func) in locals().items() \
    if callable(func) and (not __name__ == '__main__' or \
    func.__module__ == __name__)])
# stores all items() values for the previously defined methods


def multisort(guide, *data, **options):
    """
    Sorts a `guide` via criterion and then applies the same index displacement
    to all other items in `data`.

    > Parameters:

    guide : *array-like*
    The item the method will be based on to sort the additional items.

    data : *N x array-like*
    The list of items that will be sorted according to the result from the
    `guide` sort.

    criterion : *str; optional*
    Method for sorting the `guide`.
    default : 'asc'

    inplace : *bool; optional*
    Chooses whether to sort the items in-place.
    default : False

    include_guide : *bool; optional*
    If `inplace == False`, chooses whether to include `guide` into the
    returned object from the function call.
    default : True
    
    """

    kwargs = dict(
        criterion = 'asc',
        inplace = False,
        include_guide = True,
    )

    kwargs.update(options)

    for value in kwargs.keys():
        if value in options.keys() and type(kwargs[value]) \
            != type(options[value]): # quick check for kwarg validness
            raise TypeError('{} is an invalid value for {}'
                .format(options[value], value))
            return

    try:
        method = eval([name for name in ms_method_names \
            if kwargs['criterion'] in name][0])
            # similar to re.groups()
    except:
        raise IndexError('specified criterion is invalid; default set to asc')
        method = _ms_asc_ind

    sorting_indices = method(guide)
    print(('Resulting indices after sorting: {}').format(sorting_indices))

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

        return

    sorted_data = [[data_list[new_index] for new_index in sorting_indices] \
        for data_list in data]

    if kwargs['include_guide']:
        sorted_guide = [guide[new_index] for new_index in sorting_indices]
        sorted_data.insert(0, sorted_guide)

    return sorted_data

# To do:
# properly define _multidalt
# try implementing yield, with, contextmanager, for result returning
#   to avoid use of temp items
