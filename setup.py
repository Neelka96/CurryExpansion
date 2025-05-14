# Setup file used for `pip install -e`
from setuptools import setup, find_packages

setup(
    name = 'CurryInspection',
    version = '1.0.0',
    packages = find_packages(),
    install_requires = [
        'ipykernel~=6.29.5',
        'lightgbm~=4.6.0',
        'matplotlib~=3.10.3',
        'mord~=0.7',
        'pandas~=2.2.3',
        'psycopg2~=2.9.10',
        'pydantic~=2.11.4',
        'pydantic-settings~=2.9.1',
        'python-dotenv~=1.1.0',
        'PyYAML~=6.0.2',
        'scikit-learn~=1.6.1',
        'SQLAlchemy~=2.0.40',
        'SQLAlchemy-Utils~=0.41.2',
        'sodapy~=2.2.0'
    ]
)