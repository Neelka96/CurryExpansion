# Import dependencies
from pathlib import Path
from functools import lru_cache
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database, database_exists

# Custom libraries
from core.core_bin import Settings
from schemas import Base

@lru_cache()
def get_settings(**kwargs) -> Settings:
    '''Factory function for configured `Settings` object.
    
    :param  kwargs: Overwrites parsed/defaulted environment settings.
    :type   kwargs: Any

    :return:        Environment configured settings.
    :rtype:         Settings
    '''
    return Settings(**kwargs)

@lru_cache()
def get_engine(**kwargs) -> Engine:
    '''Factory function to get DB engine. Initial run creates DB and posts schema. Calls `get_settings()` factory too.

    :param  kwargs: Overwrites parsed/defaulted environment settings.
    :type   kwargs: Any
    
    :return:        SQL Alchemy configured Engine.
    :rtype:         Engine
    '''
    settings = get_settings(**kwargs)
    uri = settings.engine_uri
    if not database_exists(uri): create_database(uri)
    eng = create_engine(settings.engine_uri)
    Base.metadata.create_all(eng)
    return eng

@lru_cache
def get_session_factory(**kwargs) -> sessionmaker[Session]:
    '''Factory function to get a bound session maker. Calls `get_engine()` and therefore `get_settings()` too.

    :param  kwargs: Overwrites parsed/defaulted environment settings.
    :type   kwargs: Any

    :return:        SQL Alchemy bound session factory.
    :rtype:         sessionmaker[Session]
    '''
    engine = get_engine(**kwargs)
    return sessionmaker(bind = engine, expire_on_commit = False)


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')