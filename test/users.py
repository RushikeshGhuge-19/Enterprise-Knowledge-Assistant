from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from datetime import datetime, timezone
from test.db import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    admin = "admin"
    user = "user"
    viewer = "viewer"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
