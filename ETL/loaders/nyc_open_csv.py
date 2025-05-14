# Import dependencies
import pandas as pd
import logging
log = logging.getLogger(__name__)

from ETL.etl_bin import BaseLoader
from core import get_settings


class SaveInspectionsCSV(BaseLoader):
    def __init__(self, name: str):
        self.cfg = get_settings()
        self.p = self.cfg.storage / f'{name}.csv'

    def load(self, df: pd.DataFrame) -> None:
        df.to_csv(self.p, header = True, index = False)
        return None

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')