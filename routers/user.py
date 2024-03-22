from typing import List, Union, Optional
from fastapi import HTTPException, Depends, Query
from sqlalchemy.orm import Session
from starlette import status
from models import Users
import models
from fastapi import APIRouter
from database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

class UsersBase(BaseModel):
    id: Union[int, None] = None
    name: str
    phone_number: str
    address_id: int
    is_active: Union[bool, None] = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    role:Optional[str]=None
    

    class Config:
        orm_mode = True

class CreateUserRequest(BaseModel):
    name: str
    phone_number: str
    address_id: int

class UserUpdate(BaseModel):
    name: str
    phone_number: str
    address_id: int

# -- 1. Create New users
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UsersBase)
def create_user(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    new_user = Users(**create_user_request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# -- 2. Edit users
@router.put("/{user_id}", response_model=UsersBase)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for attr, value in user.dict(exclude_unset=True).items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# -- 3. Delete users
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = db.query(Users).filter(Users.id == user_id).first()
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {user_id} you requested for does not exist")
    db.delete(deleted_user)
    db.commit()

# -- 4. Get Single users
@router.get('/{user_id}', response_model=UsersBase, status_code=status.HTTP_200_OK)
def get_one_user(user_id: int, db: Session = Depends(get_db)):
    db_entry = db.query(Users).filter(Users.id == user_id).first()
    if db_entry is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {user_id} you requested for does not exist")
    return db_entry

# -- 5. Get all users
@router.get("/", response_model=List[UsersBase])
def get_all_addresses(db: Session = Depends(get_db)):
    return db.query(Users).all()