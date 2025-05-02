# Import Dependencies
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


# Create ORM base class
class Base(DeclarativeBase): ...


# Secondary ref table for boroughs
class Boroughs(Base):
    '''
    Represents the boroughs parent table in the database.

    Attributes:
        borough_id (String): PK representing the unique ID.
        borough (String): The boroughs's name.
        population (int): The boroughs's population.
    '''
    # Table name
    __tablename__ = 'boroughs'

    # Columns
    borough_id: Mapped[str] = mapped_column(String(2), primary_key = True)
    borough: Mapped[str] = mapped_column(nullable = False)
    population: Mapped[int] = mapped_column(nullable = True)

    # Relationships
    restaurants: Mapped[list['Restaurants']] = relationship(back_populates = 'borough')

    def __repr__(self):
        return f'<BoroughTable(id={self.borough_id}, borough={self.borough})>'


# Secondary ref table for cuisines
class Cuisines(Base):
    '''
    Represents the cuisines parent table in the database.

    Attributes:
        cuisine_id (String): PK representing the unique ID.
        cuisine (String): The name of the cuisine.
    '''
    # Table name
    __tablename__ = 'cuisines'

    # Columns
    cuisine_id: Mapped[str] = mapped_column(primary_key = True)
    cuisine: Mapped[str] = mapped_column(nullable = False)

    # Relationships
    restaurants: Mapped[list['Restaurants']] = relationship(back_populates = 'cuisine')

    def __repr__(self):
        return f'<CuisineTable(id={self.cuisine_id}, cuisine={self.cuisine})>'


# Main Table (Restaurant)
class Restaurants(Base):
    '''
    Represents the restaurants table in the database.

    Attributes:
        id (Integer): PK representing the unique ID of the location.
        name (String): The name of the location.
        borough_id (String): FK reference to Boroughs table.
        cuisine_id (String): FK reference to Cuisines table.
        inspection_date (DateTime): The date of the last inspection.
        lat (Float): The location's latitude.
        lng (Float): The location's longitude.

    Relationships:
        borough (Boroughs): Many-to-one relation to Boroughs table.
        cuisine (Cuisines): Many-to-one relation to Cuisines table.
    '''
    # Table name
    __tablename__ = 'restaurants'

    # Columns
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = False)
    borough_id: Mapped[str] = mapped_column(String(2), ForeignKey('boroughs.borough_id'), nullable = False)
    cuisine_id: Mapped[str] = mapped_column(ForeignKey('cuisines.cuisine_id'), nullable = False)
    inspection_date: Mapped[datetime] = mapped_column(nullable = False)
    lat: Mapped[float] = mapped_column(Numeric(14, 12), nullable = False)
    lng: Mapped[float] = mapped_column(Numeric(14, 12), nullable = False)

    # Relationships with reference tables, accessable through gateway now
    borough: Mapped['Boroughs'] = relationship(back_populates = 'restaurants')
    cuisine: Mapped['Cuisines'] = relationship(back_populates = 'restaurants')

    # What is shown when print or string is called on object
    def __repr__(self):
        return f'<RestaurantTable(id={self.id}, name="{self.name}")>'



# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')