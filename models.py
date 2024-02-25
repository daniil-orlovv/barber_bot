from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from bot import engine


Base = declarative_base()


class DataForRecord(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    staff = Column(String(100), nullable=False)
    service = Column(String(100), nullable=False)
    date = Column(String())
    time = Column(String())
    name = Column(String(), nullable=False)
    phone = Column(String())
    email = Column(String(100), nullable=False)
    comment = Column(String(100), nullable=True)


Base.metadata.create_all(engine)
