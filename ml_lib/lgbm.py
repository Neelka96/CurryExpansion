# Import dependencies
from lightgbm import LGBMRegressor
import numpy as np

# Define new class inherited from regressor
# Sets LGBM to clip and threshold to ensure discrete integer comptability
class LGBMOrdinal(LGBMRegressor):
    def predict(self, X):
        raw = super().predict(X)
        return np.clip(np.round(raw), 0, 2).astype(int)