from sqlalchemy import Column
from app.db.base import Base
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.sql.schema import ForeignKeyConstraint, UniqueConstraint


class Bakery(Base):
    """Model for bakery."""

    __tablename__ = "bakery"
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, nullable=False, primary_key=True)
    brand_name = Column(String(225), nullable=False)  # noqa: WPS432
    owner_id = Column(Integer, nullable=False)
    address = Column(String(225), nullable=False)
    phone = Column(String(225), nullable=False)
    description = Column(String(225), nullable=False)
    logo_url = Column(String(225), nullable=True)

    __table_args__ = (
        UniqueConstraint("brand_name", name="uq_brand_name"),
        ForeignKeyConstraint(
            ['owner_id'],
            ['user.id'],
            name="fk_bakery_owner_id"
        ),
    )

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<Bakery {brand_name!r}>".format(brand_name=self.brand_name)
