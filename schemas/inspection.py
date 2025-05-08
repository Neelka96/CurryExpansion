# Import Dependencies
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
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
            name = 'uq_inspection_natural'
        ),
    )

    # Columns
    id:                 Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    camis:              Mapped[int] = mapped_column(nullable = False)
    boro:               Mapped[str] = mapped_column(String(14), nullable = False)
    zipcode:            Mapped[int] = mapped_column(nullable = False)
    cuisine:            Mapped[int] = mapped_column(String(100), nullable = False)
    inspection_date:    Mapped[D]   = mapped_column(nullable = False)
    inspection_type:    Mapped[str] = mapped_column(String(), nullable = False)
    inspection_subtype: Mapped[str] = mapped_column(String(), nullable = False)
    action:             Mapped[str] = mapped_column(String(), nullable = False)
    violation_code:     Mapped[str] = mapped_column(String(), nullable = False)
    critical_flag:      Mapped[str] = mapped_column(String(), nullable = False)
    score:              Mapped[int] = mapped_column(nullable = False)
    census_tract:       Mapped[int] = mapped_column(nullable = False)
    nta:                Mapped[str] = mapped_column(String(), nullable = False)

    def __repr__(self):
        return f'<Inspection(id={self.id}, name="{self.score}")>'



# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')