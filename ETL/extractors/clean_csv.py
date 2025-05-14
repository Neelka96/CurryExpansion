# Import dependencies
import pandas as pd

# Abstract class to de-couple extraction classes from Pipeline
from ETL.etl_bin import BaseExtractor
from core import get_settings


class CleanedInspectionCSV(BaseExtractor):
    def __init__(self, name: str):
        self.name = name
        self.cfg = get_settings()

    def _convert_int(self, cols: list[str]):
        self.df[cols] = self.df[cols].astype(int)
        return self
    
    def _convert_flt(self, cols: list[str]):
        self.df[cols] = self.df[cols].astype(float).round(5)
        return self
    
    def _convert_dt(self, cols: list[str]):
        self.df[cols] = self.df[cols].apply(pd.to_datetime)

    def extract(self) -> pd.DataFrame:
        p = self.cfg.storage / f'{self.name}.csv'
        self.df = pd.read_csv(p)
        
        self._convert_int(['camis', 'zipcode', 'score', 'census_tract'])
        self._convert_flt(['latitude', 'longitude'])
        self._convert_dt(['inspection_date'])

        return self.df