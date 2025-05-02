import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    _instance = None

    # Singleton class instance across 1 run setup
    # Loads grouped dynamic variable initializers
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_env_vars()
            cls._instance._load_engine()
        return cls._instance
    
    # Subprivate loading methods for configuration
    def _load_env_vars(self):
        self.ENV = os.environ.get('APP_ENV', 'development').lower()
        self.NYC_OPEN_KEY = os.environ.get('NYC_OPEN_KEY')
        self.AZURE_CONN = os.environ.get('AZURE_CONN')
        self.STORAGE_ACCT_CONN = os.environ.get('STORAGE_ACCT_CONN')
        self.STORAGE = Path(os.environ.get('STORAGE', 'resources'))
        self.LOG_LEVEL = self.__get_log_level()
        self.LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
        self.SLEEP = os.environ.get('SLEEP', 1)
        self.__correct_paths()
        self.__get_references()
        return self
    
    def _load_engine(self):
        self.__get_db_name()
        self.ENGINE_PATH = self.STORAGE / self.db_name
        self.ENGINE_URI = f'sqlite:///{self.ENGINE_PATH}'
        self.UPDATE_INTERVAL = timedelta(weeks = 2)
        self.FASTFOOD_CSV = self.STORAGE / 'fastfood.csv'
        self.POPULATION_CSV = self.STORAGE / 'census_population.csv'
        return self

    # Private Methods for configuration
    def __get_db_name(self):
        if self.ENV == 'production':
            self.db_name = 'project4.sqlite'
        else:
            self.db_name = 'project4_dev.sqlite'
        return self
    
    def __get_log_level(self):
        return os.environ.get(
            'LOG_LEVEL', 'DEBUG' 
            if os.environ.get('APP_ENV') == 'development' 
            else 'INFO'
        )
    
    def __correct_paths(self):
        if self.ENV == 'production':
            pass
        else:
            repo_root = Path(__file__).resolve().parent
            self.STORAGE = repo_root / self.STORAGE
        return self
    
    def __get_references(self):
        # Transformation Constants
        REF_SEQS = {
            'BOROUGHS': (
                'Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island'
            )
            ,'CUISINES': (
                'Afghan'
                ,'African'
                ,'Armenian'
                ,'Australian'
                ,'Bangladeshi'
                ,'Basque'
                ,'Brazilian'
                ,'Cajun'
                ,'Californian'
                ,'Caribbean'
                ,'Chilean'
                ,'Chinese'
                ,'Chinese/Japanese'
                ,'Creole'
                ,'Creole/Cajun'
                ,'Czech'
                ,'Eastern European'
                ,'Egyptian'
                ,'English'
                ,'Ethiopian'
                ,'Filipino'
                ,'French'
                ,'German'
                ,'Greek'
                ,'Haute Cuisine'
                ,'Hawaiian'
                ,'Indian'
                ,'Indonesian'
                ,'Iranian'
                ,'Irish'
                ,'Italian'
                ,'Japanese'
                ,'Jewish/Kosher'
                ,'Korean'
                ,'Latin American'
                ,'Lebanese'
                ,'Mediterranean'
                ,'Mexican'
                ,'Middle Eastern'
                ,'Moroccan'
                ,'New French'
                ,'Pakistani'
                ,'Peruvian'
                ,'Polish'
                ,'Portuguese'
                ,'Russian'
                ,'Scandinavian'
                ,'Soul Food'
                ,'Southeast Asian'
                ,'Spanish'
                ,'Tapas'
                ,'Thai'
                ,'Turkish'
            )
        }


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')