from sqlalchemy import Column,Integer, String, Float

from .database import Base


class AddressBook(Base):
    """To create database address book with help of sqlalchemy """
    
    __tablename__ = 'address_book'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    address_line1 = Column(String)
    address_line2 = Column(String)
    city = Column(String)
    pincode = Column(Integer)
    latitude  = Column(Float, nullable=False)
    longitude  = Column(Float, nullable=False)


