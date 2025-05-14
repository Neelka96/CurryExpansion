# Import dependencies
import numpy as np
import pandas as pd
import scipy.sparse as sp
from typing import TypeAlias
from numpy.typing import ArrayLike

SklearnArray: TypeAlias = (
    ArrayLike
    | pd.DataFrame
    | pd.Series
    | sp.spmatrix
)

def get_metrics(
        model: object,
        X_test: SklearnArray = None,
        y_test: SklearnArray = None
    ):
    '''

    :param  model: Trained ML Model, preferably Scikit-Learn based
    :type   model: object
    :param X_test: Features testing data
    :type  X_test: SklearnArray or any array-like structure
    :param y_test: Target(s) testing data
    :type  y_test: SklearnArray or any array-like structure
    '''
    metrics = {}

    # GridSearchCV / RandomizedSearchCV
    if hasattr(model, 'best_score_'):
        metrics['best_cv_score'] = float(model.best_score_)
    if hasattr(model, 'best_params_'):
        metrics['best_params'] = model.best_params_
    if hasattr(model, 'cv_results_'):
        # Convert any arrays to lists
        cr = model.cv_results_
        metrics['cv_results'] = {
            k: (v.tolist() if hasattr(v, 'tolist') else v)
            for k, v in cr.items()
        }

    # Out‑of‑bag on ensembles
    if hasattr(model, 'oob_score_'):
        metrics['oob_score'] = float(model.oob_score_)

    # Linear model coefs/intercept
    if hasattr(model, 'coef_'):
        coefs = np.asarray(model.coef_)
        metrics['coef_mean_abs'] = float(np.mean(np.abs(coefs)))
        metrics['coef_shape'] = coefs.shape
    if hasattr(model, 'intercept_'):
        metrics['intercept'] = model.intercept_

    # Tree‐based feature importances
    if hasattr(model, 'feature_importances_'):
        metrics['feature_importances'] = model.feature_importances_.tolist()

    # Iterative solver details
    if hasattr(model, 'n_iter_'):
        metrics['n_iter'] = int(model.n_iter_)

    # Data shape info
    if hasattr(model, 'n_features_in_'):
        metrics['n_features_in'] = int(model.n_features_in_)

    # Default .score(), just in case
    if (X_test is not None) and (y_test is not None):
        try:
            metrics['test_score'] = float(model.score(X_test, y_test))
        except Exception:
            pass
    
    return metrics

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')