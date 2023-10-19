from sqlalchemy import Column
from app.db.base import Base
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.sql.schema import ForeignKeyConstraint


class Product(Base):
    """Model for product."""

    __tablename__ = "product"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(225), nullable=False)  # noqa: WPS432
    baker_id = Column(Integer, nullable=False)
    baking_time = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False, default=0)
    image_url = Column(String(225), nullable=True)
    location = Column(String(225), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['baker_id'],
            ['bakery.id'],
            name="fk_product_bakery_id"
        ),
        {'extend_existing': True}
    )

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<Product {name!r}>".format(name=self.name)
