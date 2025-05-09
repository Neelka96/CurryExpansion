# Import Dependencies
from sqlalchemy import Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal as dec
from datetime import date as D

# Bring in Base class
from schemas.base import Base


# Main Table (Restaurant)
class Inspection(Base):
    # Table name
    __tablename__ = 'inspection'
    __table_args__ = (
        UniqueConstraint(
            'camis',
            'inspection_date',
            'inspection_type',
            'inspection_subtype',
            'violation_code',
            name = 'uq_inspection_natural'
        ),
    )

    # Columns
    id:                 Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    camis:              Mapped[int] = mapped_column(nullable = False)
    boro:               Mapped[str] = mapped_column(String(15), nullable = False)
    zipcode:            Mapped[int] = mapped_column(nullable = False)
    cuisine:            Mapped[int] = mapped_column(String(35), nullable = False)
    inspection_date:    Mapped[D]   = mapped_column(nullable = False)
    inspection_type:    Mapped[str] = mapped_column(String(30), nullable = False)
    inspection_subtype: Mapped[str] = mapped_column(String(30), nullable = False)
    action:             Mapped[str] = mapped_column(String(30), nullable = False)
    violation_code:     Mapped[str] = mapped_column(String(7), nullable = False)
    critical_flag:      Mapped[str] = mapped_column(String(17), nullable = False)
    score:              Mapped[int] = mapped_column(nullable = False)
    census_tract:       Mapped[int] = mapped_column(nullable = False)
    nta:                Mapped[str] = mapped_column(String(7), nullable = False)
    latitude:           Mapped[dec] = mapped_column(Numeric(7, 5), nullable = False)
    longitude:          Mapped[dec] = mapped_column(Numeric(8, 5), nullable = False)





# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')