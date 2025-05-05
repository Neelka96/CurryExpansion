# Import dependencies
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Bring in Declarative Base
from schemas.base import Base


class DimLocation(Base):
    # Set table name
    __tablename__ = 'dim_location'

    # Columns
    ...

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')