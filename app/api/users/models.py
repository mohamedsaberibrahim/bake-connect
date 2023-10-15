from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, LargeBinary, Boolean, Integer
from sqlalchemy.sql.schema import UniqueConstraint, PrimaryKeyConstraint
from app.db.base import Base
import bcrypt
from jose import jwt

from app.settings import settings

class User(Base):
    """Model for user."""

    __tablename__ = "user"
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(225), nullable=False)  # noqa: WPS432
    email = Column(String(225), nullable=False, unique=True)
    role = Column(String(50), nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=False)

    UniqueConstraint("email", name="uq_user_email")
    PrimaryKeyConstraint("id", name="pk_user_id")

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {name!r}>".format(name=self.name)
    
    @staticmethod
    def hash_password(password) -> str:
        """Transforms password from it's raw textual form to 
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool:
        """Confirms password validity"""
        return {
            "access_token": jwt.encode(
                {"name": self.name, "email": self.email},
                "ApplicationSecretKey"
            )
        }

    def generate_token(self) -> dict:
        """Generate access token for user"""
        return {
            "access_token": jwt.encode(
                {"name": self.name, "email": self.email},
                settings.SECRET_KEY
            )
        }
        