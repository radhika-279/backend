from typing import List, Union,Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from models import Address
import models
from fastapi import APIRouter
from database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix='/address',
    tags=['Address']
)

class AddressBase(BaseModel):
    id: Union[int, None] = None
    street: str
    city: str
    state: str
    postal_code: int
    latitude: float
    longitude: float
    role:Optional[str]=None
    
    class Config:
        orm_mode = True

class CreateAddressRequest(BaseModel):
    street: str
    city: str
    state: str
    postal_code: int
    latitude: float
    longitude: float

class UpdateAddressRequest(BaseModel):
    street: str
    city: str
    state: str
    postal_code: int
    latitude: float
    longitude: float

# -- 1. Create New address
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AddressBase)
def create_address(create_address_request: CreateAddressRequest, db: Session = Depends(get_db)):
    new_address = Address(**create_address_request.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

# -- 2. Edit address
@router.put("/{address_id}", response_model=AddressBase)
def update_address(address_id: int, update_address_request: UpdateAddressRequest, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    for field, value in update_address_request.dict(exclude_unset=True).items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    return address

# -- 3. Delete address
@router.delete('/{address_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    deleted_address = db.query(Address).filter(Address.id == address_id).first()
    if deleted_address is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The address with id {address_id} does not exist")
    db.delete(deleted_address)
    db.commit()

# -- 4. Get Single address
@router.get('/{address_id}', response_model=AddressBase, status_code=status.HTTP_200_OK)
def get_one_address(address_id: int, db: Session = Depends(get_db)):
    db_entry = db.query(Address).filter(Address.id == address_id).first()
    if db_entry is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The address with id {address_id} does not exist")
    return db_entry

# -- 5. Get all addresses
@router.get("/", response_model=List[AddressBase])
def get_all_addresses(city: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        if city:
            addresses = db.query(Address).filter(Address.city == city).all()
        else:
            addresses = db.query(Address).all()
        return addresses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



