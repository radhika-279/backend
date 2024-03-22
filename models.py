from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text, Boolean, REAL
from sqlalchemy.orm import relationship
from database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(Integer, nullable=False)
    latitude = Column(REAL, nullable=False)
    longitude = Column(REAL, nullable=False)

    users = relationship("Users", back_populates="address")

    
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    is_active = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    address = relationship("Address", back_populates="users")
    



