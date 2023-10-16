from sqlalchemy import Column
from app.db.base import Base
from sqlalchemy.sql.sqltypes import String, LargeBinary, Boolean, Integer
from sqlalchemy.sql.schema import ForeignKeyConstraint, UniqueConstraint, PrimaryKeyConstraint

class Order(Base):
    """Model for order."""

    __tablename__ = "order"

    id = Column(Integer, nullable=False, primary_key=True)
    brand_name = Column(String(225), nullable=False)  # noqa: WPS432
    owner_id = Column(Integer, nullable=False)
    address = Column(String(225), nullable=False)
    phone = Column(String(225), nullable=False)
    description = Column(String(225), nullable=False)
    logo_url = Column(String(225), nullable=True)
