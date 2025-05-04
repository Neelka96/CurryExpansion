# Import dependencies
from functools import wraps
from typing import TypeVar
from types import FunctionType
from inspect import signature
import logging

def log_exceptions(fn):
    '''
    Catch *any* exception, log:
        - module.fn.qualname
        - all argument names & values
        - full traceback
    then re raise.
    '''
    # Grab the logger for the module that defined fn 
    # and the signature for the function call
    log = logging.getLogger(fn.__module__)
    sig = signature(fn)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            log.exception(
                'Exception caught in %s; args=%r',
                fn.__qualname__, bound.arguments
            )
            raise
    return wrapper

C = TypeVar('C')
def auto_log_cls(cls: type[C]) -> type[C]:
    for name, attr in cls.__dict__.items():
        if isinstance(attr, FunctionType) and not name.startswith('_'):
            setattr(cls, name, log_exceptions(attr))
    return cls

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')