from contextlib import contextmanager
import os

@contextmanager
def wdir(path):
    '''
    Yields a given path as working directory.

    Useful for importing/exporting data that's not locally stored,
    letting you not have to change the working directory back.
    For permanently changing working directory, use os.chdir(<path>)

    >>> with wdir(<path>):
    ...     <do_something>
    # sets a temporary workpath for action <do_something>
    '''

    current_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(current_dir)
