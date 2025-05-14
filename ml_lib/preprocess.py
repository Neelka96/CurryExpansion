# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt
from typing import Literal, TypeAlias
from collections.abc import Callable
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from mord import LogisticIT


TargetOptions: TypeAlias = Literal['pass-fail', 'abc-ordered']

class Helpers:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def _binning_cats(self, col: str, min: int) -> None:
        vals_to_replace = [i[0] for i in self.df[col].value_counts().items() if i[1] < min]
        self.df[col] = self.df[col].replace(vals_to_replace, 'other').astype(str)
        return self

    def _cycle_dates(self, col: str, func: Callable):
        std_vals = self.df[col].apply(func = func)
        self.df[f'{col}_sin'] = np.sin(2 * np.pi * std_vals)
        self.df[f'{col}_cos'] = np.cos(2 * np.pi * std_vals)
        return self


class InspectionPrep(Helpers):
    _NUMERICS = ['last_score', 'rolling_mean_3']
    _CYCLICALS = [
        'dow_sin', 'dow_cos', 'month_sin', 'month_cos', 'quart_sin', 'quart_cos'
    ]
    _CATEGORICALS = [
        'boro', 'zipcode', 'cuisine', 'inspection_type', 
        'inspection_subtype', 'violation_code', 'action', 
        'critical_flag', 'census_tract', 'nta', 'year', 'is_weekend'
        ]

    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.target = 'score'
    
    def _bin_all_categories(self):
        self._binning_cats('zipcode', 1000)
        self._binning_cats('census_tract', 650)
        self._binning_cats('cuisine', 300)
        self._binning_cats('violation_code', 100)
        self._binning_cats('nta', 750)
        return self
    
    def _calculate_metrics(self):
        self.df['last_score']       = self.df.groupby('camis')['score'].shift(1)
        self.df['rolling_mean_3']   = (
            self.df
                .groupby('camis')['score']
                .shift(1)
                .rolling(3)
                .mean()
                .reset_index(0, drop = True)
        )
        group_mean = self.df.groupby('camis')['score'].transform('mean')
        self.df['last_score']       = self.df['last_score'].fillna(group_mean)
        self.df['rolling_mean_3']   = self.df['rolling_mean_3'].fillna(group_mean)
        return self

    def _mk_date_fields(self):
        self.df['year']         = self.df['inspection_date'].dt.year
        self.df['month']        = self.df['inspection_date'].dt.month
        self.df['dow']          = self.df['inspection_date'].dt.weekday
        self.df['quarter']      = self.df['inspection_date'].dt.quarter
        self.df['is_weekend']   = self.df['dow'].isin([5, 6]).astype(int)
        self._cycle_dates('dow',     (lambda dow:   dow / 7         ))
        self._cycle_dates('month',   (lambda month: (month - 1) / 12))
        self._cycle_dates('quarter', (lambda quart: (quart - 1) /  4))
        return self

    def _pass_fail_bins(self) -> pd.DataFrame:
        if self.target == 'score':    
            self.df['failing'] = (self.df[self.target] >= 28).astype(int)
            self.df.drop(columns = self.target, inplace = True)
            self.target = 'failing'
            return self
        else:
            print('Could not finish. Please ensure .ordinal_bins() has not already be run.')

    def _ordinal_bins(self) -> pd.DataFrame:
        if self.target == 'score':
            bins = [-1, 13, 27, float('inf')]
            labels = [0, 1, 2]  # A=0, B=1, C=2
            self.df['grade'] = pd.cut(self.df[self.target], bins = bins, labels = labels).astype(int)
            self.df.drop(columns = [self.target], inplace = True)
            self.target = 'grade'
            return self
        else:
            print('Could not finish. Please ensure .pass_fail_bins() has not already be run.')

    def _split_everything(self):
        train_df = self.df[self.df['inspection_date'] <  self.date_cutoff]
        test_df  = self.df[self.df['inspection_date'] >= self.date_cutoff]

        self.X_train = train_df.drop(columns = ['inspection_date', self.target])
        self.y_train = train_df[self.target]

        self.X_test  = test_df.drop(columns = ['inspection_date', self.target])
        self.y_test  = test_df[self.target]
        return self
    
    def transform(self, targeting: TargetOptions, date_cutoff: str | None):
        if date_cutoff is not None:
            self.date_cutoff = pd.to_datetime(date_cutoff)
        else:
            self.date_cutoff = \
                pd.to_datetime(dt.datetime.now(dt.timezone.utc) - dt.timedelta(weeks = 12))

        self._bin_all_categories()
        self.df.sort_values(['camis', 'inspection_date'], inplace = True)
        self._calculate_metrics()
        self._mk_date_fields()
        self.df.drop(
            columns = ['id', 'month', 'dow', 'quarter', 'camis', 'latitude', 'longitude'], 
            inplace = True
        )
        if targeting == 'pass-fail':
            self._pass_fail_bins()
        elif targeting == 'abc-ordered':
            self._ordinal_bins()
        self._split_everything()
        
        prep = ColumnTransformer(
            [
                ('num', StandardScaler(), self._NUMERICS),
                ('cyc', 'passthrough', self._CYCLICALS),
                ('cat', OneHotEncoder(handle_unknown = 'ignore'), self._CATEGORICALS),
            ]
        )
        pipe = Pipeline(
            [
                ('prep', prep),
                ('clf', LogisticIT())
            ]
        )

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')