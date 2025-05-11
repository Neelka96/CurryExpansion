# Import dependencies
from pathlib import Path
from collections.abc import Callable
import pandas as pd

def find_root(
        marker_files: list[str] = [
            'setup.py',
            '.git', 
            '.gitignore', 
            '.env', 
            'README.md'
        ]
    ) -> Path:
    '''Finds resolved root path (also accessible from `Settings` object).

    :param  marker_files:   Files that agnostically indicate the root level. Defaults to standard project list.
    :type   marker_files:   list[str], optional

    :raises RuntimeError:   If no ancestor directory contains any of the marker files.

    :returns:               Resolved path to the project root.
    :rtype:                 Path
    '''
    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        if any((parent / m).exists() for m in marker_files):
            return parent
    raise RuntimeError('Could not locate project root.')


def create_dict(
        translation: Callable[[int], str]
        ,ref_list: list[str]
        ) -> dict[str, str]:
    '''Used to create lightweight reference dictionaries for transformations.

    :param  translation:    Function to map against constants.
    :type   translation:    Callable[[int], str]
    :param  ref_list:       Constants used for mappings.
    :type   ref_list:       list[str]

    :returns:               Mapped dictionary with reference ids.
    :rtype:                 dict[str, str]
    '''
    # Dictionary comprehension used to apply function to each item as it's placed in dictionary
    return {item : translation(num) for num, item in enumerate(ref_list, start = 1)}


def create_ref_table(
        mapping: dict[str, str]
        ,target_col: str
    ) -> pd.DataFrame:
    '''Readies reference/parent table for SQL insertion.

    :param  mapping:        Mapping from `create_dict()`.
    :type   mapping:        dict[str, str]
    :param  target_col:     Primary key column to be created.
    :type   target_col:     str

    :returns:               Two column table with unique IDs.
    :rtype:                 pd.DataFrame
    '''
    # Adds 'id' to target column's name to create reference ID column
    new_col = f'{target_col}_id'

    # Initializes the dataframe using dictionary pairs for values
    return pd.DataFrame(
        {
            new_col: mapping.values(),
            target_col: mapping.keys()
        }
    )

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')