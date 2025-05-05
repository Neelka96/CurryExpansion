# Import dependencies
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal as dec

# Bring in Declarative Base
from schemas.base import Base

class DimDemographic(Base):
    # Set table name
    __tablename__ = 'dim_demographic'

    # Columns
    demographic_id: Mapped[int] = mapped_column(primary_key = True)
    location_id:    Mapped[int] = mapped_column(ForeignKey('dim_location.location_id'), nullable = False)
    year:           Mapped[int] = mapped_column(nullable = False)
    median_income:  Mapped[dec] = mapped_column(Numeric(20, 2), nullable = False)
    pop_density:    Mapped[dec] = mapped_column(Numeric(20, 2), nullable = False)

    def __repr__(self):
        return f'<DimDemographic(id={self.demographic_id}, name="{self.location_id}")>'
# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')