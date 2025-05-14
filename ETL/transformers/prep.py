# Import dependencies
from collections.abc import Callable
import pandas as pd
import logging
log = logging.getLogger(__name__)

from ETL.etl_bin import BaseTransformer
from ml_lib import binning_cats, cycle_dates

class PrepTransformer(BaseTransformer):
    def __init__(self, bins: dict[str, int]):
        self.target = 'score'
        self.bins = bins

    def aggr_measures(self, roll: int):
        mean_label = f'rolling_mean_{roll}'
        self.df['last_score'] = self.df.groupby('camis')['score'].shift(1)
        self.df[mean_label] = (
            self.df
                .groupby('camis')['score']
                .shift(1)
                .rolling(roll)
                .mean()
                .reset_index(0, drop = True)
        )
        group_mean = self.df.groupby('camis')['score'].transform('mean')
        self.df['last_score'] = self.df['last_score'].fillna(group_mean)
        self.df[mean_label] = self.df[mean_label].fillna(group_mean)
        return self
    
    def cat_binner(self, bin: str, thresh: int):
        self.df = binning_cats(self.df, bin, thresh)
        self.df[bin] = self.df[bin].astype(str)
        return self
    
    def dt_cycler(self, col: str, func: Callable):
        self.df = cycle_dates(self.df, col, func)
        return self

    def create_dt_cycles(self):
        self.df['year']         = self.df['inspection_date'].dt.year
        self.df['month']        = self.df['inspection_date'].dt.month
        self.df['dow']          = self.df['inspection_date'].dt.weekday
        self.df['quarter']      = self.df['inspection_date'].dt.quarter
        self.df['is_weekend']   = self.df['dow'].isin([5, 6]).astype(int)
        self.dt_cycler('dow',     (lambda dow:   dow / 7         ))
        self.dt_cycler('month',   (lambda month: (month - 1) / 12))
        self.dt_cycler('quarter', (lambda quart: (quart - 1) /  4))
        return self
    
    def multi_class_ordinal_target(self):
        bins = [-1, 13, 27, float('inf')]
        labels = [0, 1, 2]  # A=0, B=1, C=2
        self.df['grade'] = pd.cut(self.df[self.target], bins = bins, labels = labels).astype(int)
        self.df.drop(columns = [self.target], inplace = True)
        self.target = 'grade'
        return self


    def transform(self, df: pd.DataFrame):
        self.df = df
        for bin, thresh in self.bins.items():
            self.cat_binner(bin, thresh)
        
        self.df.sort_values(['camis', 'inspection_date'], inplace = True)
        self.aggr_measures(3)
        return self.df