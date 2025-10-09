from sqlalchemy import Column, Integer, String, Date
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    profile_picture = Column(String, nullable=True)
