# Import dependencies
import sys
import subprocess

# Bring in root finder for DRY code
from core.core_bin import find_root

def trigger_venv(name: str = '.venv') -> None:
    '''
    If venv directory doesn't exist yet, invoke the bootstrap_env.py script.
    Invocation via subprocess keeps the namespace clean.

    :param venv: Customizable venv name. Defaults to '.venv'.
    :type venv: str, optional.
    '''
    # Get absolute path to root and derive venv directory too
    root = find_root()
    venv = root / name
    bootstrap = root / 'scripts' / 'bootstrap_env.py'

    if not venv.is_dir():
        # Launch bootstrap_env.py via a fresh python process - same backend command as `!python3`
        subprocess.run(
            [sys.executable, str(bootstrap), str(venv)],
            check = True,
        )

    return None


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')