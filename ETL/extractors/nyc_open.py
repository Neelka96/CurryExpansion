# Import dependencies
from sodapy import Socrata
import datetime as dt
import pandas as pd

# Abstract class to de-couple extraction classes from Pipeline
from ETL.etl_bin import BaseExtractor

class RawInspectionData(BaseExtractor):
    def __init__(self, domain: str, uri_id: str, nyc_open_key: str, years_cutoff: int, row_limit: int):
        self.uri_id = uri_id
        self.client = Socrata(domain, nyc_open_key)

        self.date_lim = (dt.datetime.now() - dt.timedelta(days = years_cutoff * 365)).isoformat()
        self.row_limit = row_limit


    def extract(self) -> pd.DataFrame:
        select_clause = (
            'camis,'
            'boro,'
            'zipcode,'
            'cuisine_description AS cuisine,'
            'inspection_date,'
            'inspection_type,'
            'action,'
            'violation_code,'
            'critical_flag,'
            'score,'
            'census_tract,'
            'nta,'
            'latitude,'
            'longitude'
        )
        where_clause = f'inspection_date > "{self.date_lim}" AND cuisine IS NOT NULL'
        return pd.DataFrame.from_records(
            self.client.get(
                self.uri_id,
                select = select_clause,
                where = where_clause,
                limit = self.row_limit
            )
        )


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')