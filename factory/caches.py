# Import dependencies
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Custom libraries
from config import Settings

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def get_engine():
    settings = get_settings()
    return create_engine(settings.engine_uri)

@lru_cache
def get_session_factory():
    engine = get_engine()
    return sessionmaker(bind = engine, expire_on_commit = False)


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')