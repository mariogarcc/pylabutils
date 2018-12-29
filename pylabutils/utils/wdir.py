from contextlib import contextmanager
import os

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

    path : str
    Path to desired working directory folder.
    """

    current_dir = os.getcwd()
    os.chdir(path) # change directory
    try:
        yield # in context
    finally: # cleanup
        os.chdir(current_dir) # back to previous directory
