# Import dependencies
import pandas as pd
from sqlalchemy.dialects.postgresql import insert

from ETL.etl_bin import BaseLoader
from core import Database, get_session_factory
from schemas import Inspection


class Load_Inspections(BaseLoader):
    def __init__(self, constraint_name):
        self.db = Database(get_session_factory())
        self.table = Inspection
        self.constraint = constraint_name

    def load(self, df: pd.DataFrame):
        rows = df.to_dict('records')
        with self.db.get_session() as session:
            stmt = insert(self.table).values(rows)
            stmt = stmt.on_conflict_do_nothing(constraint = self.constraint)
            session.execute(stmt)
        return None

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')