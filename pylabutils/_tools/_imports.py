from contextlib import contextmanager
from importlib import import_module


__all__ = ['_set_all', 'ImportGroup']



@contextmanager
def _set_all(module, new_all):
    """
    Initially planned for use inside ImportGroup to allow imports of several
    methods via `import *`.
    """
    module = import_module(module)
    old_all = module.__all__
    module.__all__ = new_all
    try:
        yield
    finally:
        module.__all__ = old_all



class ImportGroup:

    def import_method(self, module, method):
        module = __import__(
            str(module), globals(), locals(), [str(method)], 0
            )
        method = eval(f"module.{str(method)}")
        # cannot work around using eval or exec, that I know of
        return method

    def __init__(self, module, methods = []):
        for method in methods:
            setattr(self, method, self.import_method(module, method))