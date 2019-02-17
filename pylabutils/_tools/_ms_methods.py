import numpy as np

__all__ = [
    '_ms_asc_ind',
    '_ms_desc_ind',
    '_ms_dalt_ind',
    'ms_method_names',
    'ms_methods'
]


# these methods have long descriptions already, others might need them
# or we can have these descriptions deleted for being private methods
def _ms_asc_ind(item):
    """
    Sorts elements in ascending order and returns a list of their previous
    indices compared to their current ones.


    \> Parameters:

    `item` : *array-like*
    """
    if type(item) in [list, tuple]:
        myitem = [[x, item.index(x)] for x in item]
        myitem.sort() # sorts based on the first value for each pair
        return [element[1] for element in myitem] # indices

    elif type(item) == np.ndarray:
        return list(np.argsort(item)) # literally returns sorting indices

    else:
        raise ValueError("Item type not recognized")



def _ms_desc_ind(item):
    """
    Sorts elements in descending order and returns a list of their previous
    indices compared to their current ones.


    \> Parameters:

    `item` : *array-like*
    """
    if type(item) in [list, tuple]:
        myitem = [[x, item.index(x)] for x in item]
        myitem.sort(reverse = True)
        return [element[1] for element in myitem]

    elif type(item) == np.ndarray:
        return list(np.argsort(item))[::-1]

    else:
        raise ValueError("Item type not recognized")


# redo this one, but no one will use it yet
def _ms_dalt_ind(item):
    """
    Sorts elements in a sign-alternating descending order and returns a list
    of their previous indices compared to their current ones.

    
    \> Parameters:

    `item` : *array-like*
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
