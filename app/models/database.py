from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.config.settings import settings

Base = declarative_base()
engine = create_engine(settings.database_url, connect_args={""check_same_thread"": False})
SessionLocal = sessionmaker(bind=engine)

class TransactionType(PyEnum):
    INCOME = ""income""
    EXPENSE = ""expense""

class User(Base):
    __tablename__ = ""users""
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    transactions = relationship(""Transaction"", back_populates=""owner"")

class Transaction(Base):
    __tablename__ = ""transactions""
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String(200))
    category = Column(String(50))
    transaction_type = Column(Enum(TransactionType))
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey(""users.id""))
    owner = relationship(""User"", back_populates=""transactions"")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
