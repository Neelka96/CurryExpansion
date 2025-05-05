# Import dependencies
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal as dec
from datetime import date

# Bring in Declarative Base
from schemas.base import Base

class FactFeature(Base):
    # Set table name
    __tablename__ = 'fact_feature'

    # Columns
    feature_id:     Mapped[int]     = mapped_column(primary_key = True)
    location_id:    Mapped[int]     = mapped_column(ForeignKey('dim_location.location_id'), nullable = False)
    cuisine_id:     Mapped[int]     = mapped_column(ForeignKey('dim_cuisine.cuisine_id'), nullable = False)
    run_date:       Mapped[date]    = mapped_column(nullable = False)
    competitors:    Mapped[int]     = mapped_column(nullable = False)
    demand_gap:     Mapped[dec]     = mapped_column(Numeric(), nullable = False)
    median_income:  Mapped[dec]     = mapped_column(Numeric(), nullable = False)
    pop_density:    Mapped[dec]     = mapped_column(Numeric(), nullable = False)

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')