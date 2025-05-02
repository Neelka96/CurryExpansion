import os
from pathlib import Path
from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict

# API keys removed from settings as they're included in expansion of the YAML
class Settings(BaseSettings):
    APP_ENV: str = 'development'    # needs a .lower() method
    LOG_LEVEL: str = 'INFO'         # needs a dynamic implementation based off env
    LOG_FILE: str = 'app.log'
    DEBUG: bool
    SLEEP: int = 1
    
    STORAGE: Path


    model_config = SettingsConfigDict(
        env_file = '.env'
    )

#     def _load_env_vars(self):
#         self.AZURE_CONN = os.environ.get('AZURE_CONN')
#         self.STORAGE_ACCT_CONN = os.environ.get('STORAGE_ACCT_CONN')
#         self.STORAGE = Path(os.environ.get('STORAGE', 'resources'))
#         self.__correct_paths()
#         self.__get_references()
#         return self

#     def _load_engine(self):
#         self.__get_db_name()
#         self.ENGINE_PATH = self.STORAGE / self.db_name
#         self.ENGINE_URI = f'sqlite:///{self.ENGINE_PATH}'
#         self.UPDATE_INTERVAL = timedelta(weeks = 2)
#         self.FASTFOOD_CSV = self.STORAGE / 'fastfood.csv'
#         self.POPULATION_CSV = self.STORAGE / 'census_population.csv'
#         return self

#     # Private Methods for configuration
#     def __get_db_name(self):
#         if self.ENV == 'production':
#             self.db_name = 'project4.sqlite'
#         else:
#             self.db_name = 'project4_dev.sqlite'
#         return self

#     def __correct_paths(self):
#         if self.ENV == 'production':
#             pass
#         else:
#             repo_root = Path(__file__).resolve().parent
#             self.STORAGE = repo_root / self.STORAGE
#         return self



# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')