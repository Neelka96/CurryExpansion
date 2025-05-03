from typing import Literal, Any, TypeAlias
from pathlib import Path

from pydantic import SecretStr, model_validator, field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Type aliases to make improve readability of Settings fields
Envs: TypeAlias = Literal['development', 'production']
LogLevels: TypeAlias    = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET']

# Quick FYI for reading of configuration
# Pydantic's BaseSettings validators works in the flow of: 
# (mode = 'before') model -> field -> (mode = 'after') field -> model

class Settings(BaseSettings):
    # Base options
    model_config = SettingsConfigDict(env_file = None, case_sensitive = False)

    # API keys removed from settings as they're included in expansion of the YAML
    # Basic App/Env Configurations
    app_env:        Envs                = 'development'
    debug:          bool                = True

    # Log Configurations
    log_level:      LogLevels           = 'INFO'
    log_name:       str                 = 'app'

    # Drives available to store persistent data and the drive chosen by user or default for environment
    mnt_drive:      Path                = Path('/mnt/shared')
    loc_drive:      Path                = Path(__file__).resolve().parent / 'resources'

    # CaaS secrets
    caas_conn:      SecretStr | None    = None  # Default of None -> (Prod) **REQUIRED | (Dev) None
    caas_mnt_conn:  SecretStr | None    = None  # ^^^ Same as above

    # PostgreSQL URI construction parts - db_user_pass ALWAYS REQUIRED
    db_user_name:   str                 = 'curryexp'
    db_user_pass:   SecretStr
    db_name:        str                 = 'curryexpander'
    db_host:        str                 = 'localhost'
    db_port:        int                 = 5432


    # 1) -- Pre parsing field validators --
    # Specifically lowercases on app env
    @classmethod
    @field_validator('app_env', mode = 'before')
    def _lowercase_strings(cls, v: Any) -> Any:
        return v.lower() if isinstance(v, str) else v
    
    # Specifically uppercases on log level
    @classmethod
    @field_validator('log_level', mode = 'before')
    def _uppercase_strings(cls, v: Any) -> Any:
        return v.upper() if isinstance(v, str) else v
    
    # Strips whitespace on string values that may be alphanumeric
    @classmethod
    @field_validator('*', mode = 'before')
    def _strip_all_strings(cls, v: Any) -> Any:
        return v.strip() if isinstance(v, str) else v
    

    # 2) -- Post parsing model validation --
    @model_validator(mode = 'after')
    def _extra_post_validation(self) -> 'Settings':
        # Checks for presence of cloud service connection strings and raises if error if any are missing
        if self.app_env == 'production' and (self.caas_conn is None or self.caas_mnt_conn is None):
            raise TypeError('CaaS connection strings required in production settings.')
        return self


    # 3) -- Post parsing property fields dumped into Pydantic --
    # storage property comes from the active environment and whether or not the drive exists; if production mount doesn't exist switch to development mount
    @computed_field
    @property
    def storage(self) -> Path:
        if self.app_env == 'production' and self.mnt_drive.exists() and self.mnt_drive.is_dir():
            return self.mnt_drive
        else:
            if not self.loc_drive.exists():
                self.loc_drive.mkdir(parents = True, exist_ok = True)
            return self.loc_drive

    # log_file property comes from other dynamic property configured during runtime
    @computed_field
    @property
    def log_file(self) -> Path:
        log_path = self.storage / self.log_name
        log_path = log_path.with_suffix(log_path.suffix + '.log')
        return log_path

    # engine_uri property comes from other static environment variable configurations available
    @computed_field
    @property
    def engine_uri(self) -> str:
        eng = 'postgresql+psycopg2'
        return f'{eng}://{self.db_user_name}:{self.db_user_pass.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}'


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')