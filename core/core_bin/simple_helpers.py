# Import dependencies
from pathlib import Path
from functools import lru_cache

@lru_cache
def find_root(marker_files: list[str] = ['.git', '.gitignore', '.env', 'README.md']) -> Path:
    '''Simple helper function at the base level to find the project root.

    :param marker_files: Defaults to ['pyproject.toml', 'setup.py', '.git', '.gitignore', '.env', 'README.md'].
    :type  marker_files: list[str], optional

    :raises RuntimeError: If no ancestor directory contains any of the marker files.

    :returns: The path to your project root.
    :rtype: Path
    '''
    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        if any((parent / m).exists() for m in marker_files):
            return parent
    raise RuntimeError('Could not locate project root.')


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')