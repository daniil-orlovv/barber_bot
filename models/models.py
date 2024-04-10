from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


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
    record_hash = Column(String(100))


class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    id_ycl = Column(String(10))
    name = Column(String())
