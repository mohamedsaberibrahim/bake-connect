from sqlalchemy import Column
from app.db.base import Base
from sqlalchemy.sql.sqltypes import String, LargeBinary, Boolean, Integer, DateTime
from sqlalchemy.sql.schema import ForeignKeyConstraint, UniqueConstraint, PrimaryKeyConstraint

class Order(Base):
    """Model for order."""

    __tablename__ = "order"

    id = Column(Integer, nullable=False, primary_key=True)
    payment_method = Column(String(255), nullable=False)
    bakery_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    state = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    tracking_number = Column(String(16), nullable=False)
    start_baking_at = Column(DateTime, nullable=False)
    finish_baking_at = Column(DateTime, nullable=False)
    cancelled_at = Column(DateTime, nullable=True)


    __table_args__ = (
        ForeignKeyConstraint(
            ['bakery_id'],
            ['bakery.id'],
            'fk_order_bakery_id'
        ),
        ForeignKeyConstraint(
            ['product_id'],
            ['product.id'],
            'fk_order_product_id'
        ),
        ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
            'fk_order_user_id'
        ),
        UniqueConstraint(
            'tracking_number',
            name='uq_order_tracking_number'
        ),
    )