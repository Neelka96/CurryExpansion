# Import dependencies
import pandas as pd

# Abstract class to de-couple extraction classes from Pipeline
from etl_bin import BaseExtractor

class NYC_Restaurants(BaseExtractor):
    def __init__(self):
        ...

    def extract(self) -> pd.DataFrame:
        ...



# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')