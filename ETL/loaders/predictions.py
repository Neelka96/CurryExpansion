# Import dependencies
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
import json
import logging
log = logging.getLogger(__name__)

# Abstract class to de-couple extraction classes from Pipeline
from ETL.etl_bin import BaseLoader
from core import get_settings
from ml_lib import LGBMOrdinal

class MakePredictions(BaseLoader):
    def __init__(self, name: str):
        log.info('Loading in serialized pipeline.')
        self.cfg = get_settings()
        pipe_path = self.cfg.storage / f'{name}.joblib'
        self.model: Pipeline = joblib.load(pipe_path)


    def _predictions(self):
        log.debug('Making predictions using model.')
        self.preds = self.model.predict(self.df)
        self.probs = self.model.predict_proba(self.df).tolist()
        return self
    
    def _build_json(self):
        log.debug('Crafting JSON for metadata.')
        output = []
        self.df = self.df.reset_index().rename(columns={'index': 'inspection_id'})
        for idx, (row_id, pred, prob) in enumerate(zip(self.df['inspection_id'], self.preds, self.probs)):
            output.append({
                'inspection_id': int(row_id),
                'predicted_score': int(pred),
                'probabilities': prob
            })
        with open('predictions.json', 'w') as f:
            json.dump(output, f, indent=2)
        log.info(f'Wrote {len(output)} predictions to predictions.json')


    def load(self, df: pd.DataFrame) -> None:
        log.info('Starting model load.')
        self.df = df
        self._predictions()
        self._build_json()
        return None