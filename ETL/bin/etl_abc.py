# Import dependencies
from abc import ABC, abstractmethod
import pandas as pd

# Bring in log exception handler
from ext_lib import log_exceptions
# An important note:
#   - log_exceptions should only be used as a wrapper to handle exceptions that bubble up
#   - all other helper methods should be denoted with the single underscore '_' and be called by the predefined methods


class BaseExtractor(ABC):
    @log_exceptions
    @abstractmethod
    def extract(self) -> pd.DataFrame: ...

class BaseTransformer(ABC):
    @log_exceptions
    @abstractmethod
    def transform(self) -> pd.DataFrame: ...

class BaseLoader(ABC):
    @log_exceptions
    @abstractmethod
    def load(self) -> None: ...


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')