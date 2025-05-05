# Import dependencies
from math import ceil
from contextlib import contextmanager
from collections.abc import Sequence, Generator
from sqlalchemy import Select, Row, insert
from sqlalchemy.sql import Executable
from sqlalchemy.orm import DeclarativeMeta, sessionmaker, Session
import pandas as pd

# Custom libraries
from .core_bin import auto_log_cls

# Create logger
import logging
log = logging.getLogger(__name__)


# Composition based class definition
@auto_log_cls
class Database:
    '''In housed session management and basic db solutions.
    Session and engine management created from factories to prevent duplicates.

    get_session() is the primary usage for object, however other methods are wrapped via get_session() too.
    '''
    def __init__(self, session_factory: sessionmaker[Session]):
        self.session_factory = session_factory

    # Context management handler for sessions for centralized handling
    @contextmanager
    def get_session(self) -> Generator[Session]:
        '''Custom session context manager for SQL Alchemy.

        Yields:
            Generator[SessionType]: New session from bound engine connection pool.
        '''
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

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
            result = session.execute(stmt, params) if params else session.execute(stmt)
            return result.scalars().all() if isinstance(stmt, Select) else None

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
        # Insert the table from scratch via chunks in case of large size
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

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')