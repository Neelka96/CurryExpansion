# Import dependencies
import pandas as pd


class Targeting:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.target = 'score'

    def pass_fail_bins(self) -> pd.DataFrame:
        if self.target == 'score':    
            self.df['failing'] = (self.df[self.target] >= 28).astype(int)
            self.df.drop(columns = self.target, inplace = True)
            self.target = 'failing'
            return self
        else:
            print('Could not finish. Please ensure .ordinal_bins() has not already be run.')

    def ordinal_bins(self) -> pd.DataFrame:
        if self.target == 'score':
            bins = [-1, 13, 27, float('inf')]
            labels = [0, 1, 2]  # A=0, B=1, C=2
            self.df['grade'] = pd.cut(self.df[self.target], bins = bins, labels = labels).astype(int)
            self.df.drop(columns = [self.target], inplace = True)
            self.target = 'grade'
            return self
        else:
            print('Could not finish. Please ensure .pass_fail_bins() has not already be run.')

    def target_split(self) -> tuple[pd.DataFrame, pd.Series]:
        return self.df.drop(columns = [self.target]), self.df[self.target]


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')