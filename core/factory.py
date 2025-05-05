# Import dependencies
from functools import lru_cache
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

# Custom libraries
from .core_bin import Settings

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(settings.engine_uri)

@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    engine = get_engine()
    return sessionmaker(bind = engine, expire_on_commit = False)


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')