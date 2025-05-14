# Import dependencies
import pandas as pd

# Abstract class to de-couple extraction classes from Pipeline
from ETL.etl_bin import BaseTransformer


class EmptyTransformer(BaseTransformer):
    def __init__(self):
        pass

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df