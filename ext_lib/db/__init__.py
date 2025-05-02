from .database import Database
from .schema import Base
import pkgutil
import importlib

__all__ = []

for finder, name, is_pkg in pkgutil.walk_packages(__path__, prefix = __name__ + '.'):
    module = importlib.import_module(name)

    for attr in dir(module):
        obj = getattr(module, attr)
        if isinstance(obj, type) and issubclass(obj, Base) and obj and not Base:
            globals()[attr] = obj
            __all__.append(attr)


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')