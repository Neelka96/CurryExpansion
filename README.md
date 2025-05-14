# CurryInspection: Restaurant Inspection Score Prediction
**Module:** Final Project  
**Bootcamp:** EdX(2U) & UT Data Analytics and Visualization Bootcamp  
**Cohort:** Cohort UTA-VIRT-DATA-PT-11-2024-U-LOLC  
**Authors:**  
Neel Kumar Agarwal,  
Samora Machel,  
Rob LaPreze,  
Manny Guevara  


## Table of Contents

1. [Quick Run for Grader](#quick-run-for-grader)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [ETL Pipeline](#etl-pipeline)
6. [Machine Learning](#machine-learning)
7. [Usage & Demonstration](#usage--demonstration)
8. [Scripts](#scripts)
9. [Results](#results)
10. [Contributing & Future Work](#contributing--future-work)
11. [License & Acknowledgments](#license--acknowledgments)

---

## Quick Run for Grader

For a fast end-to-end validation, your TA can:

```bash
# 1. Bootstrap environment
python scripts/bootstrap_env.py .venv

# 2. Execute ETL stage or full pipeline
# Specify a single task:
python scripts/run_etl.py extract  
# Or run full pipeline (defaults to ETL/pipeline.yml):
python scripts/run_etl.py pipeline

# 3. Launch Part 2 notebook
jupyter lab Notebooks/Part2.ipynb
```

> **Estimated total runtime:** \~30 minutes total
>
> * ETL stages: \~10 minutes
> * Model training & tuning (notebook): \~15 minutes
> * Notebook rendering: \~5 minutes

---

## Getting Started

### Prerequisites

* **Python 3.10+** (Conda recommended)
* **Git** for version control

### Installation & Bootstrapping

```bash
# 1. Clone the repository
git clone https://github.com/your-username/CurryInspection.git
cd CurryInspection

# 2. Create virtual environment and install dependencies\python scripts/bootstrap_env.py .venv

# 3. Activate the environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# 4. Verify imports
python -c "import core, ETL, ml_lib"
```

### Starting from the Notebooks

If grading begins in the notebook:

1. Open `Part1.ipynb` in Jupyter Lab.
2. Run the first two cells to install dependencies and create `.venv` automatically.
3. Restart the Jupyter kernel and select the new `.venv` environment.
4. Continue running the remaining cells.

---

## Project Structure

```text
CurryInspection/
├── core/                   # Core utilities (config, logging, factories)
├── ETL/                    # Pipeline library & pipeline.yml (default path: ETL/pipeline.yml)
├── ml_lib/                 # Shared ML helpers (metrics, models, preprocess)
├── Notebooks/              # Jupyter notebooks (Part1.ipynb, Part2.ipynb)
├── resources/              # Data artifacts & logs (optional)
├── scripts/                # Executables: bootstrap_env.py, run_etl.py, exec_pipeline.py
├── setup.py                # setuptools configuration
└── README.md               # Project documentation
```

> **Note:** The `schemas/` directory contains legacy PostgreSQL schema definitions from an earlier implementation and is not required for the current pipeline setup. Additionally, metadata folders (`CurryInspection.egg-info/`, `__MACOSX/`, `.DS_Store`) are project artifacts and do not impact functionality.

> **Ignored:** `schemas/`, `CurryInspection.egg-info/`, `__MACOSX/`, `.DS_Store`

---

## Configuration

Two primary configuration sources:

1. **`core/config.py`**

   ```python
   # core/core_bin/config.py
   from pydantic import BaseSettings, Field
   from pathlib import Path

   class Settings(BaseSettings):
       db_url: str = Field(..., env='DB_URL')
       storage: Path = Path('resources')
       log_level: str = 'INFO'

       class Config:
           env_file = '.env'
   ```

   * Override via `.env`:

     ```ini
     DB_URL=postgresql://user:pass@localhost:5432/inspections
     LOG_LEVEL=DEBUG
     ```

2. **`ETL/pipeline.yml`** (default location: `CurryInspection/ETL/pipeline.yml`)

   ```yaml
   # ETL/pipeline.yml
   extractors:
     nyc_open:
       class: ETL.extractors.nyc_open.RawInspectionData
       params:
         domain: 'data.cityofnewyork.us'
         uri_id: '43nn-pn8j'
         nyc_open_key: ${env:nyc_open_key}
         years_cutoff: 7
         row_limit: 1000000
     quick_csv:
       class: ETL.extractors.nyc_open_csv.CSVPredictionLoader
       params: {}

   transformers:
     date_engineer:
       class: ETL.transformers.prep.DateEngineer
       params: {}
     passthrough:
       class: ETL.transformers.passthrough.Passthrough
       params: {}

   loaders:
     postgres:
       class: ETL.loaders.nyc_open.PostgresLoader
       params:
         table: inspections
     make_predictions:
       class: ETL.loaders.model.ModelPredictionLoader
       params:
         model_path: resources/models/final_model.joblib

   tasks:
     get_data_csv:
       pipelines: [ quick_csv, date_engineer, postgres ]
     grid_tune_train:
       pipelines: [ quick_csv, date_engineer, postgres, fresh_train ]
     get_predictions:
       pipelines: [ quick_csv, make_predictions ]

   default: pipeline
   ```

---

## ETL Pipeline

Pipeline stages inherit from abstract base classes under `ETL/etl_bin/etl_abc.py` and are wired via `pipeline.yml`.

### Example Extractor

```python
# ETL/extractors/nyc_open.py
from ETL.etl_bin.etl_abc import BaseExtractor
import pandas as pd

class RawInspectionData(BaseExtractor):
    def extract(self):
        # Fetch JSON records from Socrata
        records = self.client.get(
            domain=self.params['domain'],
            dataset=self.params['uri_id'],
            limit=self.params['row_limit'],
            where=f"inspection_date >= '{self.params['years_cutoff']} years ago'"
        )
        self.df = pd.DataFrame(records)
        return self
```

### Running ETL

* **Single task:**

  ```bash
  python scripts/run_etl.py extract
  ```
* **Full pipeline (default):**

  ```bash
  python scripts/run_etl.py pipeline --config ETL/pipeline.yml
  ```

Intermediate DataFrames are saved as Parquet under `resources/processed/` by default.

---

## Machine Learning

### Data Preparation & Splitting

In `Notebooks/ml_training.ipynb`, we use a time-aware split:

```python
from sklearn.model_selection import TimeSeriesSplit

# Setup 3-fold time-based CV for grid search
tscv = TimeSeriesSplit(n_splits=3)

# Later, in GridSearchCV:
from ml_lib.gridder import GridSearchCV, kappa_scorer
lgbm_search = GridSearchCV(
    estimator=ml_pipeline,
    param_grid=lgbm_grid,
    cv=tscv,
    scoring=kappa_scorer,
    n_jobs=7
)
lgbm_search.fit(X_train, y_train)
```

### Model Definitions

Custom ordinal regressor in `ml_lib/lgbm.py`:

```python
# ml_lib/lgbm.py
from lightgbm import LGBMRegressor
import numpy as np

class LGBMOrdinal(LGBMRegressor):
    """
    Extends LGBMRegressor to produce discrete scores {0,1,2} by rounding.
    """
    def predict(self, X):
        raw = super().predict(X)
        return np.clip(np.round(raw), 0, 2).astype(int)
```

### Stacking Ensemble

Constructed in `Notebooks/ml_training.ipynb`:

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import RidgeClassifier
from ml_lib.lgbm import LGBMOrdinal
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.base import clone

# Prepare estimators
estimators = [
    ('lgbm', LGBMOrdinal(random_state=42, verbosity=-1)),
    ('rf', RandomForestClassifier(random_state=42, class_weight='balanced'))
]

# Initialize stacking classifier
stack_clf = StackingClassifier(
    estimators=estimators,
    final_estimator=RidgeClassifier(alpha=1.0),
    cv=3,
    passthrough=False
)

# Build full pipeline
full_pipe = Pipeline([
    ('preprocessor', column_transformer),
    ('stack', stack_clf)
])

# Fit ensemble
full_pipe.fit(X_train, y_train)
```

---

## Usage & Demonstration

1. **Run ETL & train**:

   ```bash
   python scripts/run_etl.py pipeline
   ```
2. **Open notebooks**:

   ```bash
   jupyter lab Notebooks/Part1.ipynb
   ```
3. **Export figures**:.

   * Learning curves: saved in `Notebooks/figures/learning_curves.png`
   * Feature importances: `Notebooks/figures/feature_importance.png`
4. **View logs**:

   * Pipeline and model logs: `resources/logs/pipeline.log`

---

## Scripts

### `bootstrap_env.py`

Bootstraps environment:

```bash
python scripts/bootstrap_env.py .venv
# Creates .venv/, installs core, ETL, and ml_lib in editable mode
# Also installs notebook dependencies
```

### `run_etl.py`

CLI for ETL pipeline:

```bash
# Run a single task:
python scripts/run_etl.py <task_name>  
# Run full pipeline (default ETL/pipeline.yml):
python scripts/run_etl.py pipeline
```

### `exec_pipeline.py`

(Alternate runner combining ETL + ML)

```bash
python scripts/exec_pipeline.py --config pipeline.yml --stages extract,transform,load,train
```

---

## Results

**Classification Report (Test Set):**

```
              precision    recall  f1-score   support

           0       0.85      0.87      0.86      6705
           1       0.89      0.84      0.86      5708
           2       0.91      0.92      0.92      9199

    accuracy                           0.89     21612
   macro avg       0.88      0.88      0.88     21612
weighted avg       0.89      0.89      0.89     21612
```

**Additional Metrics:**

* Cohen’s Kappa Score: 0.8244
* Generalization Gap (accuracy): -0.0191
* Mean Absolute Error (train): 0.1712
* Mean Absolute Error (test): 0.1591
* Quadratic Weighted Kappa (train): 0.8271
* Quadratic Weighted Kappa (test): 0.8297

**Confusion Matrix (Test Set):**

```
[[ 5844   671   190]
 [  915  4787  1006]
 [  201   683  8315]]
```

Top 5 feature importances:

1. Number of violations
2. Cuisine type embedding
3. Days since last inspection
4. Borough one-hot encoding
5. Inspection type

Visual outputs in `Notebooks/figures/`.

---

## Contributing & Future Work

* **Swap ETL logic:** Modify `ETL/pipeline.yml` or pass a different config path.
* **Extend models:** Add new classes to `ml_lib/models.py` and reference in notebooks.
* **Cloud/CICD:** Dockerize and integrate GitHub Actions for automatic grading.

---

## References

* NYC Open Data API: [https://dev.socrata.com/foundry/data.cityofnewyork.us/43nn-pn8j](https://dev.socrata.com/foundry/data.cityofnewyork.us/43nn-pn8j)
* Python Documentation: [https://docs.python.org/3/](https://docs.python.org/3/)
* pandas Documentation: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
* Matplotlib Documentation: [https://matplotlib.org/stable/contents.html](https://matplotlib.org/stable/contents.html)
* scikit-learn Documentation: [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)
* mord (Ordinal Regression) Documentation: [https://github.com/fabianp/mord](https://github.com/fabianp/mord)
* LightGBM Documentation: [https://lightgbm.readthedocs.io/](https://lightgbm.readthedocs.io/)
* Project README & website assistance by OpenAI ChatGPT
