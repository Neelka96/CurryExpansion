# Import dependencies
from typing import TypeAlias
from numpy.typing import ArrayLike
import pandas as pd
import scipy.sparse as sp

SklearnArray: TypeAlias = (
    ArrayLike
    | pd.DataFrame
    | pd.Series
    | sp.spmatrix
)

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')