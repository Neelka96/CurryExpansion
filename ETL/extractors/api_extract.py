# Import dependencies
import pandas as pd

# Abstract class to de-couple extraction classes from Pipeline
from ext_lib import BaseExtractor

class NYC_Open_Extractor(BaseExtractor):
    def __init__(self):
        ...

    def extract(self) -> pd.DataFrame:
        ...



# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')