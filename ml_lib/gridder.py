# Import dependencies
from sklearn.metrics import classification_report, mean_absolute_error, cohen_kappa_score
from sklearn.model_selection import GridSearchCV, learning_curve
from contextlib import redirect_stderr, contextmanager
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import ast
import os

# Bring in Core
from core import find_root

# Boiler plate for warning supression
@contextmanager
def suppress_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        with open(os.devnull, 'w') as devnull:
            with redirect_stderr(devnull):
                yield

def _get_clf_report(search_obj: GridSearchCV, X_te, y_te):
    with suppress_warnings():
        print(classification_report(y_te, search_obj.predict(X_te)))
    return None

def _get_est_scores(search_obj: GridSearchCV, X_te, y_te):
    with suppress_warnings():
        print(
            f'Best Params: {search_obj.best_params_}\n'
            f'Best Score: {search_obj.best_score_}\n'
            f'Test Accuracy: {search_obj.score(X_te, y_te)}'
        )
    return None

# More boiler plate to get scoring for best estimators and conversion from grid to dataframe
def fast_est_scores(search_obj, Xy_dict: dict[str, pd.DataFrame]):
    X_te = Xy_dict['X_te']
    y_te = Xy_dict['y_te']
    _get_clf_report(search_obj, X_te, y_te)
    _get_est_scores(search_obj, X_te, y_te)
    return None

def full_est_scores(search_grid: GridSearchCV, Xy_dict: dict[str, pd.DataFrame]):
    est = getattr(search_grid, 'best_estimator_', search_grid)
    X_tr = Xy_dict['X_tr']
    y_tr = Xy_dict['y_tr']
    X_te = Xy_dict['X_te']
    y_te = Xy_dict['y_te']
    with suppress_warnings():
        cohen_scr = cohen_kappa_score(y_te, est.predict(X_te))
        train_acc = est.score(X_tr, y_tr)
        test_acc = est.score(X_te, y_te)
        y_pred_train = est.predict(X_tr)
        y_pred_test  = est.predict(X_te)

    print(f'Cohen Kappa Score: {cohen_scr}')
    print(f'Gen Gap (acc): {train_acc - test_acc}')
    print('MAE train:', mean_absolute_error(y_tr, y_pred_train))
    print('MAE test: ', mean_absolute_error(y_te,  y_pred_test))
    print('QWK (Cohen’s kappa) train:', cohen_kappa_score(y_tr, y_pred_train, weights='quadratic'))
    print('QWK test: ', cohen_kappa_score(y_te,  y_pred_test, weights='quadratic'))


def grid_to_pd(grid: GridSearchCV) -> pd.DataFrame:
    cols = [
        'params', 'mean_fit_time', 
        'std_fit_time', 'mean_score_time', 
        'std_score_time', 'mean_test_score', 
        'std_test_score', 'rank_test_score'
    ]
    df = pd.DataFrame(grid.cv_results_, columns = cols)
    full_params = pd.json_normalize(df['params'])
    clf = full_params.pop('clf')
    df['params'] = full_params.apply(lambda row: row.dropna().to_dict(), axis = 1)

    return pd.concat([clf, df], axis = 1).copy()



# After reading in CSV, use parse params to convert back into real object
def _parse_params(cell: str) -> dict:
    if not isinstance(cell, str):
        return {}
    params = ast.literal_eval(cell)
    return params

# Expand df takes in a dataframe and applies parse_params and expands the dataframe
def expand_csv(file_name = 'grid_log.csv'):
    df = pd.read_csv(find_root() / file_name)
    df['params'] = df['params'].apply(_parse_params)
    params = pd.json_normalize(df['params'])

    df.drop(columns = ['params'], inplace = True)
    return pd.concat([df, params], axis = 1)


def read_write_grid(search_grid: GridSearchCV, file_name = 'grid_log.csv', overwrite = False):
    path = find_root() / file_name
    df = grid_to_pd(search_grid)
    if not overwrite:
        if path.is_file():
            csv_df = pd.read_csv(path)
            csv_df['params'] = csv_df['params'].apply(_parse_params)
            df = pd.concat([csv_df, df], axis = 0)
        df.to_csv(path, header = True, index = False)
    else:
        df.to_csv(path, header = True, index = False)
    return None

def learning_curve_plot(
        name: str, search_grid: GridSearchCV, Xy_dict: dict[str, pd.DataFrame], cv: int = 5
    ):
    est = getattr(search_grid, 'best_estimator_', search_grid)
    X_tr = Xy_dict['X_tr']
    y_tr = Xy_dict['y_tr']
    with suppress_warnings():
        train_sizes, train_scores, val_scores = learning_curve(
            est, X_tr, y_tr, cv = cv, train_sizes=[.1, .3, .5, .7, 1.0]
        )

    # learning_curve_df.plot.line(x = 'training_scores', y = 'val_scores')
    # Compute means and stds across folds
    train_mean = train_scores.mean(axis=1)
    train_std  = train_scores.std(axis=1)
    val_mean   = val_scores.mean(axis=1)
    val_std    = val_scores.std(axis=1)

    # Plot
    plt.fill_between(
        train_sizes, 
        train_mean - train_std,
        train_mean + train_std, 
        alpha=0.1
    )
    plt.fill_between(
        train_sizes, 
        val_mean   - val_std,
        val_mean   + val_std,   
        alpha=0.1
    )

    plt.plot(train_sizes, train_mean, label='Training score')
    plt.plot(train_sizes, val_mean,   label='Validation score')

    plt.xlabel('Number of training examples')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig('name', dpi = 300, bbox_inches = 'tight')
    plt.show()
    return None