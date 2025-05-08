import csv
import json
import uuid
from pathlib import Path
import datetime as dt

class Log_Training:
    '''
        Logs experiments to a per-user CSV. Each row contains:
        - timestamp (ISO)
        - run_id (UUID4)
        - model_name (class name)
        - params (JSON dict)
        - metrics (JSON dict)
        - extra (JSON dict for anything else you want to track)
    '''

    def __init__(self, classmate_name: str, log_dir = Path('logs')):
        self.classmate = classmate_name
        log_dir.mkdir(exist_ok = True)
        log_stem = f'{classmate_name}_models.csv'
        self.log_path = log_dir / log_stem

        # If the file doesn’t exist, write a header
        # if not os.path.isfile(self.log_path):
        if not self.log_path.is_file():
            with open(self.log_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp','run_id','model_name','params','metrics','extra'])

    def log(self,
            model=None,
            *,
            model_name: str = None,
            params: dict = None,
            metrics: dict = None,
            extra: dict = None):
        '''
        Write one experiment record.

        If you pass a scikit‑learn–style `model`, its .get_params() will be recorded automatically.
        Otherwise, supply model_name and params explicitly.
        '''
        # Determine the name
        name = model_name or (model.__class__.__name__ if model is not None else '<unknown>')

        # Get params
        if params is None:
            if model is not None and hasattr(model, 'get_params'):
                params = getattr(model, 'get_params')
            else:
                try:
                    params = getattr(model, '__dict__', {})
                except:
                    params = {}
        # Default metrics/extra
        metrics = metrics or {}
        extra   = extra   or {}
        row = [
            dt.datetime.now(dt.UTC).isoformat(),
            str(uuid.uuid4()),
            name,
            json.dumps(params,  separators=('',','':'), default=str),
            json.dumps(metrics, separators=(',',':'), default=str),
            json.dumps(extra,   separators=(',',':'), default=str),
        ]

        with open(self.log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

        return None
