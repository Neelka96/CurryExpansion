# Import Dependencies
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Bring in Base class
from schemas.base import Base


# Main Table (Restaurant)
class DimRestaurant(Base):
    # Table name
    __tablename__ = 'dim_restaurant'

    # Columns
    restaurant_id:  Mapped[int] = mapped_column(primary_key = True)
    name:           Mapped[str] = mapped_column(String(75), nullable = False)
    cuisine_id:     Mapped[int] = mapped_column(ForeignKey('dim_cuisine.cuisine_id'), nullable = False)
    location_id:    Mapped[int] = mapped_column(ForeignKey('dim_location.location_id'), nullable = False)
    address:        Mapped[str] = mapped_column(String(100), nullable = False)

    # Relationships with reference tables, accessable through gateway now
    # borough: Mapped['Boroughs'] = relationship(back_populates = 'restaurants')
    # cuisine: Mapped['Cuisines'] = relationship(back_populates = 'restaurants')

    def __repr__(self):
        return f'<DimRestaurant(id={self.restaurant_id}, name="{self.name}")>'



# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')