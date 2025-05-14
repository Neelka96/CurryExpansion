# Import dependencies
import pandas as pd
import logging
log = logging.getLogger(__name__)

from ETL.etl_bin import BaseTransformer

class InspectionCleaner(BaseTransformer):
    def __init__(self):
        log.info('InspectionCleaner constructed successfully.')

    def _map_actions(self):
        self.action_map = {
            'Violations were cited in the following area(s).': 'cited_violation',
            'Establishment Closed by DOHMH. Violations were cited in the following area(s) and those requiring immediate action were addressed.': 'cited_violations_and_closed',
            'No violations were recorded at the time of this inspection.': 'no_violations',
            'Establishment re-opened by DOHMH.': 'reopened',
            'Establishment re-closed by DOHMH.': 'reclosed'
        }
        self.df['action'] = self.df['action'].map(self.action_map)
        log.debug('_map_actions() finished.')
        return self

    def _split_into_two_columns(self, cols: list[str]):
        self.df[cols] = (
            self.df[cols[0]]
            .str
                .split('/', n = 1, expand = True)
            .rename(
                columns = {0: cols[0], 1: cols[1]}
            )
        )
        for col in cols:
            self.df[col] = self.df[col].str.strip()

        cols = list(self.df.columns)
        new_order = cols[:6]
        new_order.extend(reversed(cols[-2:]))
        new_order.extend(cols[6:-2])

        self.df = self.df[new_order]
        log.debug('_split_into_two_columns finished.')
        return self
    
    def _fill_nulls(self, row_mask: pd.Series, target: str, fill: int | str):
        self.df.loc[row_mask, target] = self.df.loc[row_mask, target].fillna(fill)
        return self

    def _convert_int(self, cols: list[str]):
        self.df[cols] = self.df[cols].astype(int)
        return self
    
    def _convert_flt(self, cols: list[str]):
        self.df[cols] = self.df[cols].astype(float).round(5)
        return self

    def _convert_dt(self, cols: list[str]):
        self.df[cols] = self.df[cols].apply(pd.to_datetime)
        return self
    

    def _null_handler(self):
        null_score = (self.df['score'].isna())
        masks = [
            ((self.df['critical_flag'] == 'Not Applicable') & (null_score)),
            ((self.df['action'] == 'no_violations') & (null_score)),
            ((self.df['violation_code'].isna()) & (null_score))
        ]
        for mask in masks:
            self._fill_nulls(mask, 'score', '0')
        
        self._fill_nulls(self.df['violation_code'].isna(), 'violation_code', 'None')
        log.debug('_null_handler() finished.')
        return self


    def transform(self, df: pd.DataFrame):
        self.df = df
        log.info('Beginning transformations. DataFrame is of shape %s.' % str(self.df.shape))
        
        # Maps actions taken for inspections into much smaller phrases | Splits the inspection column by type/subtype
        self._map_actions()
        self._split_into_two_columns(['inspection_type', 'inspection_subtype'])

        # Readies the df for null filling by converting everything to string type
        self.df = self.df.convert_dtypes()

        # Filling as many nulls as possible using the knowledge of the dataset
        self._null_handler()

        # Dropping any rows with a null field and converting all datatypes explicitly
        self.df.dropna(how = 'any', inplace = True)
        self._convert_int(['camis', 'zipcode', 'score', 'census_tract'])
        self._convert_flt(['latitude', 'longitude'])
        self._convert_dt(['inspection_date'])
        
        log.debug('All datatypes converted properly.')
        log.info('Transformations successful! DataFrame is of shape %s.' % str(self.df.shape))
        return self.df


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')