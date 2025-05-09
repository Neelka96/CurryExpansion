# Import dependencies
from sqlalchemy.orm import class_mapper
import pandas as pd

# Abstract class to de-couple extraction classes from Pipeline
from ETL.etl_bin import BaseExtractor
from core import Database, get_session_factory
from schemas import Inspection


class Postgres_Features(BaseExtractor):
    def __init__(self):
        self.db = Database(get_session_factory())

    def _convert_int(self, cols: list[str]):
        self.df[cols] = self.df[cols].astype(int)
        return self
    
    def _convert_flt(self, cols: list[str]):
        self.df[cols] = self.df[cols].astype(float).round(5)
        return self
    
    def _convert_dt(self, cols: list[str]):
        self.df[cols] = self.df[cols].apply(pd.to_datetime)

    def _prepare_for_pandas(self, data: list[Inspection]):
        cols = [r.key for r in class_mapper(Inspection).columns]
        data = [dict(zip(cols, [getattr(row, col) for col in cols])) for row in data]
        self.df = pd.DataFrame(data)
        return self

    def extract(self) -> pd.DataFrame:
        with self.db.get_session() as session:
            results = session.query(Inspection).all()

        self._prepare_for_pandas(results)
        
        self._convert_int(['camis', 'zipcode', 'score', 'census_tract'])
        self._convert_flt(['latitude', 'longitude'])
        self._convert_dt(['inspection_date'])

        return self.df