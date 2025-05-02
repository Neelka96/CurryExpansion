from typing import Literal, Any
from pathlib import Path
from datetime import timedelta

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# API keys removed from settings as they're included in expansion of the YAML
class Settings(BaseSettings):
    APP_ENV: str = 'development'
    LOG_LEVEL:          Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET'] | None = 'INFO' # Default by env -> (Prod) INFO | (Dev) DEBUG
    DEBUG:              bool        = True
    SLEEP:              int         = 1
    UPDATE_INTERVAL:    int | None  = None

    STORAGE:            Path | None = None  # Default by env    -> (Prod) /mnt/shared   | (Dev) /~/resources
    LOG_FILE:           Path | None = None  
    AZURE_CONN:         str | None  = None  # Default of None   -> (Prod) Required str  | (Dev) None
    STORAGE_ACCT_CONN:  str | None  = None

    ENGINE_NAME:        str | None  = 'curryexpanse'
    ENGINE_PATH:        Path | None = None
    ENGINE_URI:         Path | None = None


    model_config = SettingsConfigDict(
        env_file = '.env'
        # ,env_ignore_empty = True
        ,case_sensitive = False
    )

    @field_validator('LOG_LEVEL', mode = 'before')
    def uppercase_log_level(cls, v: Any) -> Any:
        if isinstance(v, str):
            return v.upper().strip()
        return v

    @field_validator('APP_ENV', mode = 'before')
    def lowercase_app_env(cls, v: Any) -> Any:
        if isinstance(v, str):
            return v.lower().strip()
        return v

    @field_validator(mode = 'after')
    def new_post_type_coersion_here(cls, v: Any) -> Any:
        ...
    
    @model_validator(mode = 'after')
    def dynamic_settings(cls, v: dict) -> dict:
        env = v['APP_ENV']  # Shorthand for environment setting

        # Raises error if the Azure Conn Str is mising in production
        if env == 'production' and v['AZURE_CONN'] is None:
            raise TypeError('Cloud provider connection string required for production environments.')

        # # Dynamic default for log level by env
        # if v['LOG_LEVEL'] is None:
        #     v['LOG_LEVEL'] = 'INFO' if env == 'production' else 'DEBUG'
        
        # Dynamic default for storage directory by env
        if v['STORAGE'] is None:
            v['STORAGE'] = Path('/mnt/shared') if env == 'production' else Path(__file__).resolve().parent / 'resources'

        # 
        if v['LOG_FILE'] is None: 
            v['LOG_FILE'] = 'app.log'
        v['LOG_FILE'] = v['STORAGE'] / v['LOG_FILE']

        if v['ENGINE_PATH'] is None:
            v['ENGINE_PATH'] = v['STORAGE'] / 'postgresql+psycopg2://local:host@localhost:5432/curryexpanse'

#     def _load_engine(self):
#         self.ENGINE_PATH = self.STORAGE / self.db_name
#         self.ENGINE_URI = f'sqlite:///{self.ENGINE_PATH}'
#         self.UPDATE_INTERVAL = timedelta(weeks = 2)
#         self.FASTFOOD_CSV = self.STORAGE / 'fastfood.csv'
#         self.POPULATION_CSV = self.STORAGE / 'census_population.csv'
#         return self


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')