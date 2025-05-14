# Import dependencies
import pandas as pd
import logging
log = logging.getLogger(__name__)

from ETL.etl_bin import BaseLoader
from core import get_settings


class SaveInspectionsCSV(BaseLoader):
    def __init__(self):
        self.cfg = get_settings()

    def load(self, df: pd.DataFrame) -> None:
        p = self.cfg.storage / self.cfg.clean_csv_stem
        df.to_csv(p, header = True, index = False)
        return None

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')