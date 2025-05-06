# Import dependencies
import pandas as pd

from etl_bin import BaseTransformer

class Transformer(BaseTransformer):
    def __init__(self, df: pd.DataFrame):
        self.df = df.dropna(how = 'any')
    
    def _map_actions(self):
        self.action_map = {
            'Violations were cited in the following area(s).': 'cited_violation',
            'Establishment Closed by DOHMH. Violations were cited in the following area(s) and those requiring immediate action were addressed.': 'cited_violations_and_closed',
            'No violations were recorded at the time of this inspection.': 'no_violations',
            'Establishment re-opened by DOHMH.': 'reopened',
            'Establishment re-closed by DOHMH.': 'reclosed'
        }
        self.df['action'] = self.df['action'].map(self.action_map)

    def transform(self):
        self._map_actions()
        return self.df

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')