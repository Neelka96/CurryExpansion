# Import dependencies
from sklearn.ensemble import StackingClassifier
import pandas as pd
import joblib
import json
import logging
log = logging.getLogger(__name__)

# Abstract class to de-couple extraction classes from Pipeline
from ETL.etl_bin import BaseLoader
from core import get_settings


class MakePredictions(BaseLoader):
    def __init__(self, name: str):
        self.cfg = get_settings()
        self.p = self.cfg.storage / f'{name}.joblib'
        self.model: StackingClassifier = joblib.load(self.p)

    def _predictions(self):
        self.preds = self.model.predict(self.df)
        self.probs = self.model.predict_proba(self.df).tolist()
        return self
    
    def _build_json(self):
        output = []
        for idx, (row_id, pred, prob) in enumerate(zip(self.df['inspection_id'], self.preds, self.probs)):
            output.append({
                'inspection_id': int(row_id),
                'predicted_score': int(pred),
                'probabilities': prob
            })

        with open('predictions.json', 'w') as f:
            json.dump(output, f, indent=2)

        log.info(f'Wrote {len(output)} predictions to predictions.json')

    def transform(self, df: pd.DataFrame) -> None:
        self.df = df
        self._predictions()
        self._build_json()
        return None