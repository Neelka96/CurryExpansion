# Import dependencies
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
import logging
log = logging.getLogger(__name__)

from ETL.etl_bin import BaseLoader
from core import Database, get_session_factory, get_settings
from schemas import Inspection


class InspectionsLoader(BaseLoader):

    def __init__(self, constraint_name: str):
        log.info('Load_Inspections constructed with constraint: %s.' % constraint_name)
        self.db = Database(get_session_factory())
        self.cfg = get_settings()
        self.constraint = constraint_name

    def load(self, df: pd.DataFrame):
        log.debug('Loading DataFrame of shape %s to db %s.', str(df.shape), self.cfg.db_name)
        rows = df.to_dict('records')
        try:
            with self.db.get_session() as session:
                stmt = insert(Inspection).values(rows)
                stmt = stmt.on_conflict_do_nothing(constraint = self.constraint)
                session.execute(stmt)
            log.info('Loading to Inspections table successful!')
        except Exception:
            log.critical('Could not data into postgres. Critical failure, exiting early.')
        finally:
            return None

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')