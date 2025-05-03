# Import dependencies
from math import ceil
from contextlib import contextmanager
from collections.abc import Sequence, Generator
from sqlalchemy import event, Engine, Select, Row, create_engine, insert
from sqlalchemy.orm import DeclarativeMeta, sessionmaker, Session as Session_Class
from sqlalchemy.sql import Executable
import pandas as pd

# Import configuration
from config.config import Config
config = Config()

# Create logger
import logging
log = logging.getLogger(__name__)

# Import protocols
from .protocols import DBAPI_Connection


# Single engine instance for class blueprint
engine = create_engine(config.ENGINE_URI)

# Event listener for engine connection, enforces foreign keys upon connection
@event.listens_for(Engine, 'connect')
def enforce_sqlite_fks(dbapi: DBAPI_Connection, conn_record) -> None:
    cursor = dbapi.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close()
    return None

# Bind session to engine now that modifications to engine are done
SessionLocal = sessionmaker(bind = engine, expire_on_commit = False)


# Composition based class definition
class Database:
    def __init__(self):
        self.__session = SessionLocal

    # Context management handler for sessions for centralized handling
    @contextmanager
    def get_session(self) -> Generator[Session_Class]:
        '''Custom session context manager for SQL Alchemy.

        Yields:
            Generator[SessionType]: New session from bound engine connection pool.
        '''
        session = self.__session()
        try:
            yield session
            session.commit()
            log.debug('Session successfully committed.')
        except Exception:
            session.rollback()
            log.critical('Session rollback from error.')
            raise 
        finally:
            session.close()
            log.debug('Closing session.')

    # Utility for executing session requests
    def execute_query(
            self
            ,stmt: Executable
            ,params: dict | Sequence[dict] | None = None
            ) -> Sequence[Row] | None:
        '''Wrapper for custom context manager for simple and bulk queries.

        :param stmt: A core SQL clause `Select`, `Insert`, `Delete`, ...
        :type stmt: Executable
        :param params: Data or constraints to be used. Defaults to None.
        :type params: dict | Sequence[dict] | None

        :returns: Returns view of data from `Select` type.
        :rtype: Sequence[Row]
        :returns: Non-select executable type returns 0.
        :rtype: int
        '''
        with self.get_session() as session:
            log.debug('execute_query() called.')
            try:
                result = session.execute(stmt, params) if params else session.execute(stmt)
                log.debug('execute_query() successful run.')
                return result.scalars().all() if isinstance(stmt, Select) else None
            except Exception:
                log.exception('Could not run execute_query().')
                raise

    def fresh_table(
            self
            ,tableClass: DeclarativeMeta
            ,df: pd.DataFrame
            ) -> None:
        '''Creates new table, expects it to be empty.

        :param tableClass: Staged table.
        :type tableClass: DeclarativeMeta
        :param df: Data to write to table.
        :type df: pd.DataFrame

        :returns: Rows changed.
        :rtype: int
        '''
        log.debug('Building fresh table.')
        try:    # Insert the table from scratch via chunks in case of large size
            chunk_size = int(1e4)
            total_rows = df.shape[0]
            num_chunks = ceil(total_rows / chunk_size)
            rows_added = 0

            stmt = insert(tableClass)
            for i in range(num_chunks):
                chunk = df.iloc[i * chunk_size : (i+1) * chunk_size]
                rows_added += chunk.shape[0]
                self.execute_query(stmt, chunk.to_dict('records')) # Combining of insert() from core w/ session.execute() utilizes ORM layer
            log.debug('Table built successfully. %s rows.', rows_added)
            return None
        except Exception:
            log.exception('Could not build fresh table.')
            raise

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')