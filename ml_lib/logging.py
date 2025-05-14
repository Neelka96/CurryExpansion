# Import dependencies
import csv
import json
import uuid
from datetime import datetime as dt, timezone as tz

# Bring in settings to configure the path
from core import get_settings
from ml_lib.scoring import get_metrics, SklearnArray

_JSON_DUMPS = lambda data: json.dumps(data, separators = (',', ':'), default = str)

class ExperimentLogger:
    '''
        Logs experiments to a per-user CSV. **Please construct once and use continuously for all model training and testing.**

        :param name: Your name which will be added to the front of the log file name.
        :type name: str
    '''
    _FIELDS = ['timestamp', 'run_id', 'model_name', 'params', 'metrics', 'extra']

    def __init__(self, name: str):
        log_dir = get_settings().storage / 'ml_logs'
        log_dir.mkdir(parents = True, exist_ok = True)
        self.log_path = log_dir / f'{name}_models.csv'

        # If the file doesn’t exist, write a header
        if not self.log_path.exists():
            with self.log_path.open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames = self._FIELDS)
                writer.writeheader()

    def _merge_metrics(
            self,
            auto_metrics: dict,
            user_metrics: dict
        ) -> dict:
        cleaned = {}
        for k, v in user_metrics.items():
            if k in auto_metrics:
                cleaned[f'user_{k}'] = v
            else:
                cleaned[k] = v
        return {**auto_metrics, **cleaned}

    def log(
            self,
            model: object,
            X_test: SklearnArray = None,
            y_test: SklearnArray = None,
            *,
            params: dict = None,
            metrics: dict = None,
            extra: dict = None
        ) -> None:
        '''
        Write one experiment record.

        If you pass a scikit‑learn–style `model`, its .get_params() and as many metrics as possible will be recorded automatically.
        Otherwise, supply params and metrics explicitly.
        '''
        # Determine the name
        name = model.__class__.__name__ if model is not None else '<unknown>'

        # Parameters: if None try to call get_params()
        if params is None:
            if model is not None and hasattr(model, 'get_params'):
                try:
                    params = model.get_params()
                except Exception:
                    # Some models require args, fall back
                    params = {}
            else:
                params = {}

        # Get all metrics available
        user_metrics    = metrics or {}
        auto_metrics    = get_metrics(model, X_test, y_test)

        # Combine and set extras up if available
        all_metrics     = self._merge_metrics(auto_metrics, user_metrics)
        extra           = extra or {}

        row = {
            'timestamp':    dt.now(tz.utc).isoformat(),
            'run_id':       str(uuid.uuid4()),
            'model_name':   name,
            'params':       _JSON_DUMPS(params),
            'metrics':      _JSON_DUMPS(all_metrics),
            'extra':        _JSON_DUMPS(extra)
        }

        # Append to CSV
        with self.log_path.open('a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = self._FIELDS)
            writer.writerow(row)
        return None


    # def train_and_log_mord(self, X, y, test_size, **mord_kwargs):
    #     Xtr, Xte, ytr, yte = train_test_split(X, y, test_size = test_size, stratify = y)
    #     m = mord.LogisticIT(**mord_kwargs).fit(Xtr, ytr)
    #     preds = m.predict(Xte)
    #     metrics = {'accuracy': accuracy_score(yte, preds)}
    #     self.log(model=m, metrics=metrics)
    #     return print(metrics)


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')