# Import dependencies
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal as dec

# Bring in Declarative Base
from schemas.base import Base


class DimLocation(Base):
    # Set table name
    __tablename__ = 'dim_location'

    # Columns
    location_id:    Mapped[int] = mapped_column(primary_key = True)
    city:           Mapped[str] = mapped_column(String(30), nullable = False)
    state:          Mapped[str] = mapped_column(String(15), nullable = False)
    zipcode:        Mapped[int] = mapped_column(nullable = False)
    census_tract:   Mapped[dec] = mapped_column(Numeric(), nullable = False)
    latitude:       Mapped[dec] = mapped_column(Numeric(6, 4), nullable = False)
    longitude:      Mapped[dec] = mapped_column(Numeric(7, 4), nullable = False)


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')