# Import dependencies
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Bring in Declarative Base
from schemas.base import Base

# Secondary ref table for cuisines
class DimCuisine(Base):
    # Table name
    __tablename__ = 'dim_cuisine'

    # Columns
    cuisine_id:     Mapped[int] = mapped_column(primary_key = True)
    cuisine_name:   Mapped[str] = mapped_column(String(50), nullable = False)
    category:       Mapped[str] = mapped_column(String(50), nullable = False)

    # Relationships
    # restaurants: Mapped[list['Restaurants']] = relationship(back_populates = 'cuisine')

    def __repr__(self):
        return f'<DimCuisine(id={self.cuisine_id}, cuisine={self.cuisine_name})>'

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')