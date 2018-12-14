import copy
import numpy as np

def _asc_ind(item):
    """
    Sorts elements in ascending order and returns a list of their previous
    indices compared to their current ones.

    Parameters:

    item : array-like
    """
    if type(item) in [list, tuple]:
        myitem = [[x, item.index(x)] for x in item]
        myitem.sort()
        return [element[1] for element in myitem]

    elif type(item) == np.ndarray:
        return list(np.argsort(item))

    else:
        return 'Item type not recognized'


def _desc_ind(item):
    """
    Sorts elements in descending order and returns a list of their previous
    indices compared to their current ones.

    Parameters:

    item : array-like
    """
    if type(item) in [list, tuple]:
        myitem = [[x, item.index(x)] for x in item]
        myitem.sort(reverse = True)
        return [element[1] for element in myitem]

    elif type(item) == np.ndarray:
        return list(np.argsort(item))[::-1]

    else:
        return 'Item type not recognized'


def _dalt_ind(item):
    """
    Sorts elements in a sign-alternating descending order and returns a list
    of their previous indices compared to their current ones.

    Parameters:

    item : array-like
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

methods = [name for (name, func) in locals().items() \
    if callable(func) and (not __name__ == '__main__' or \
    func.__module__ == __name__)]

def multisort(guide, *data, **options):
    """
    Sorts various indexable objects to a criterion that only one of them
    (the guide) follows.

    > Parameters:

    guide : *array-like*
    The item the method will be based on to sort the additional items.

    data : *N x array-like*
    The list of items that will be sorted according to the result from the
    `guide` sort.

    criterion : *str, optional*
    Method for sorting the `guide`.
    default : 'asc'

    inplace : *bool, optional*
    Chooses whether to sort the items in-place.
    default : False

    include_guide : *bool, optional*
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
        if value in options.keys() and type(kwargs[value]) != type(options[value]):
            raise TypeError('{} is an invalid value for {}'
                .format(kwargs[value], value))
            return

    try:
        method = eval([name for name in methods if kwargs['criterion'] in name][0])
    except:
        raise IndexError('specified criterion is invalid; default set to asc')
        method = _asc_ind

    sorted_indices = method(guide)
    print(('Resulting indices after sorting: {}').format(sorted_indices))

    if len(data) == 1:
        data = data[0]

    if kwargs['inplace']:

        for data_list in data:
            temp_list = copy.copy(data_list)
            for index in range(len(data_list)):
                data_list[index] = temp_list[sorted_indices[index]]

        if kwargs['include_guide']:
            temp_guide = copy.copy(guide)
            for index in range(len(guide)):
                guide[index] = temp_guide[sorted_indices[index]]

        return

    sorted_data = [[data_list[new_index] for new_index in sorted_indices] \
        for data_list in data]

    if kwargs['include_guide']:
        sorted_guide = [guide[new_index] for new_index in sorted_indices]
        sorted_data.insert(0, sorted_guide)

    return sorted_data

# To do:
# properly define _multidalt
# try implementing yield, with, contextmanager, for result returning
#   to avoid use of temp items
