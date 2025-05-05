# Import dependencies
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal as dec

# Bring in Declarative Base
from schemas.base import Base

class FactRecommendation(Base):
    # Set table name
    __tablename__ = 'fact_recommendations'

    # Columns
    recommendation_id:  Mapped[int]     = mapped_column(primary_key = True)
    prediction_id:      Mapped[int]     = mapped_column(ForeignKey('fact_prediction.prediction_id'))
    is_selected:        Mapped[bool]    = mapped_column(nullable = False)
    expected_revenue:   Mapped[dec]     = mapped_column(Numeric(), nullable = False)
    expected_rating:    Mapped[dec]     = mapped_column(Numeric(), nullable = False)

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')