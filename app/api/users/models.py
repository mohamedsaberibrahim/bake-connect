from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, LargeBinary, Boolean, Integer
from sqlalchemy.sql.schema import UniqueConstraint
from app.db.base import Base


class User(Base):
    """Model for user."""

    __tablename__ = "user"
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(225), nullable=False)  # noqa: WPS432
    email = Column(String(225), nullable=False)
    role = Column(String(50), nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {name!r}>".format(name=self.name)
