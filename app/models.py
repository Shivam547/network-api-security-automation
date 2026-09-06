from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    active = Column(Boolean, default=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False, default="PENDING")
    # Optimistic locking
    version = Column(Integer, nullable=False, default=1)

    # Temporary resource locking
    locked_by = Column(String(100), nullable=True)
    lock_expires_at = Column(DateTime, nullable=True)