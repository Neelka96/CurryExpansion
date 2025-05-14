# Import dependencies
from typing import Literal, Any, TypeAlias
from pathlib import Path

# pydantic specific dependencies
from pydantic import SecretStr, model_validator, field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project helpers
from core.core_bin.tools import find_root

# Type aliases to make improve readability of Settings fields
Envs:       TypeAlias   = Literal['development', 'production']
LogLevels:  TypeAlias   = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET']

# Quick FYI for reading of configuration
# Pydantic's BaseSettings validators works in the flow of: 
# Pre construct model, field -> Post construct field, model -> computed fields

class Settings(BaseSettings):
    # Base options
    model_config = SettingsConfigDict(env_file = '.env', case_sensitive = False)

    # API keys removed from settings as they're included in expansion of the YAML
    # Basic App/Env Configurations
    app_env:        Envs                = 'development'
    debug:          bool                = True
    root:           Path                = find_root()

    # Log Configurations
    log_level:      LogLevels           = 'INFO'
    log_name:       str                 = 'app'

    # Drives available to store persistent data and the drive chosen by user or default for environment
    mnt_drive:      Path                = '/mnt/shared'
    loc_drive_stem: Path                = root / 'resources'

    # CaaS secrets
    caas_conn:      SecretStr | None    = None  # Default of None -> (Prod) **REQUIRED | (Dev) None
    caas_mnt_conn:  SecretStr | None    = None  # ^^^ Same as above

    # Replacing Postgres save with CSV save for ease
    clean_csv_stem: str                 = 'clean_inspection_data.csv'
    ml_log_stem:    str                 = 'grid_log.csv'
    model_stem:     str                 = 'curry_inspector.h5'

    # PostgreSQL URI construction parts
    db_user_name:   str                 = 'postgres'
    db_user_pass:   SecretStr           = 'postgres'
    db_name:        str                 = 'postgres'
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
    def _conn_str_validation(self) -> 'Settings':
        # Checks for presence of cloud service connection strings and raises if error if any are missing
        if self.app_env == 'production' and (self.caas_conn is None or self.caas_mnt_conn is None):
            raise TypeError('CaaS connection strings required in production settings.')
        return self


    # 3) -- Post parsing property fields dumped into Pydantic --
    # BP code - directory helper function
    # Fixes the path and creates directory if it doesn't exist
    def _mkdir_get_path(self, stem: Path) -> Path:
        p = self.root / stem
        p.mkdir(parents = True, exist_ok = True)
        return p


    # 4) -- Computed field creation after full object construction --
    @computed_field
    @property
    def loc_drive(self) -> Path:
        return self._mkdir_get_path(self.loc_drive_stem)

    # storage property comes from the active environment and whether or not the drive exists; if production mount doesn't exist switch to development mount
    @computed_field
    @property
    def storage(self) -> Path:
        if self.app_env == 'production' and self.mnt_drive.exists() and self.mnt_drive.is_dir():
            p = self.mnt_drive
        else:
            p = self.loc_drive
        return p

    # log_file property comes from other dynamic property configured during runtime
    @computed_field
    @property
    def log_file(self) -> Path:
        p = self.storage / self.log_name
        p = p.with_suffix(p.suffix + '.log')
        return p

    # engine_uri property comes from other static environment variable configurations available
    @computed_field
    @property
    def engine_uri(self) -> str:
        eng = 'postgresql+psycopg2'
        return f'{eng}://{self.db_user_name}:{self.db_user_pass.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}'

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')