# Import depedencies
from functools import reduce
import pandas as pd

from etl_bin import BaseTransformer


class Merge(BaseTransformer):
    def __init__(self, dfs: list[pd.DataFrame], on: str | list[str], how = 'inner'):
        self.on = on
        self.how = how
        self.dfs = dfs
    
    def transform(self):
        expr = lambda left, right: pd.merge(left, right, how = self.how, on = self.on)
        return reduce(expr, self.dfs)