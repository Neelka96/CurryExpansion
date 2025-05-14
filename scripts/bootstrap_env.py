#!/usr/bin/env python3
import sys
import venv
import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path

# CLI class for namespace linking and linter assistance
class CLIArgs(Namespace):
    venv_name: str


# Absolute root path finder
def find_root(marker_files: str = ['setup.py', '.git', '.gitignore', '.env', 'README.md']) -> Path:
    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        if any((parent / m).exists() for m in marker_files):
            return parent
    raise RuntimeError('Could not locate project root.')


# Called by main() when executing the file. This is the main payload.
def create_env(venv_name: str):
    # Check for windows OS
    win32 = True if sys.platform == 'win32' else False
    
    # Get root and the venv directory
    root = find_root()
    venv_dir = root / venv_name

    # Create venv directory with pip if it doesn't exist 
    if not venv_dir.exists():
        print(f'Creating a venv in: {venv_dir}')
        venv.EnvBuilder(with_pip = True).create(str(venv_dir))
    else:
        print(f'A venv already exists in: {venv_dir}')
    
    # Build pip executable based on the OS
    if win32:
        python_exe = venv_dir / 'Scripts' / 'python.exe'
    else:
        python_exe = venv_dir / 'bin' / 'python'
    
    # Installing packages into venv including project subpackages
    print('Installing packages in editable mode.')
    subprocess.check_call([str(python_exe), '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([str(python_exe), '-m', 'pip', 'install', '-e', str(root)])

    # Printing out usage instructions for venv or restarting in Jupyter Notebooks
    print('\nSetup complete!')
    if win32:
        text = f'{venv_name}\\Scripts\\activate' 
    else:
        text = f'source {venv_name}/bin/activate'
    print(f'Please restart kernel to select new environment, or activate in CLI via:  {text}')
    
    return None

# Parse arguments, callable from the CLI or runnable as a subprocess now!
def main():
    parser = ArgumentParser(
        description = 'Bootstrap a Python venv and install your package in editable mode'
    )
    parser.add_argument(
        'venv_name',
        nargs = '?',
        default = '.venv',
        help = 'Name of the virtual‑env folder to create (default: .venv).'
    )
    args = parser.parse_args(namespace = CLIArgs())
    create_env(args.venv_name)
    return None


if __name__ == '__main__':
    main()