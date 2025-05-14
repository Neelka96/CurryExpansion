# Import dependencies
from collections.abc import Callable
import pandas as pd
import numpy as np


def binning_cats(df: pd.DataFrame, col: str, min: int) -> pd.DataFrame:
    vals_to_replace = [i[0] for i in df[col].value_counts().items() if i[1] < min]
    df[col] = df[col].replace(vals_to_replace, 'other').astype(str)
    return df

def cycle_dates(df: pd.DataFrame, col: str, func: Callable) -> pd.DataFrame:
    std_vals = df[col].apply(func = func)
    df[f'{col}_sin'] = np.sin(2 * np.pi * std_vals)
    df[f'{col}_cos'] = np.cos(2 * np.pi * std_vals)
    return df