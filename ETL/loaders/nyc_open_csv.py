# Import dependencies
import pandas as pd
import logging
log = logging.getLogger(__name__)

from ETL.etl_bin import BaseLoader
from core import get_settings


class InspectionsLoader(BaseLoader):

    def __init__(self):
        self.cfg = get_settings()

    def load(self, df: pd.DataFrame):
        p = self.cfg.clean_csv_stem
        

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')