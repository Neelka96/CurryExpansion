# Import dependencies
from sodapy import Socrata
import datetime as dt
import pandas as pd

# Abstract class to de-couple extraction classes from Pipeline
from etl_bin import BaseExtractor

class Restaurant_Inspection(BaseExtractor):
    def __init__(self, domain: str, uri_id: str, api_key: str, years_cutoff: int, row_limit: int):
        self.uri_id = uri_id
        self.client = Socrata(domain, api_key)

        self.date_lim = (dt.datetime.now() - dt.timedelta(days = years_cutoff * 365)).isoformat()
        self.row_limit = row_limit


    def extract(self) -> pd.DataFrame:
        select_clause = (
            'camis AS id,'
            'boro,'
            'zipcode,'
            'cuisine_description AS cuisine,'
            'inspection_date,'
            'action,'
            'violation_code,'
            'critical_flag,'
            'score,'
            'record_date,'
            'inspection_type,'
            'census_tract,'
            'nta'
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