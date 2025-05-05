# Import dependencies
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal as dec
from datetime import datetime as dt

# Bring in Declarative Base
from schemas.base import Base

class FactPrediction(Base):
    # Set table name
    __tablename__ = 'fact_prediction'

    # Column
    prediction_id:  Mapped[int] = mapped_column(primary_key = True)
    feature_id:     Mapped[int] = mapped_column(ForeignKey('fact_feature.feature_id'), nullable = False)
    model_version:  Mapped[str] = mapped_column(String(15), nullable = False)
    score:          Mapped[dec] = mapped_column(Numeric(7, 7), nullable = False)
    at_time:        Mapped[dt]  = mapped_column(nullable = False)


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')