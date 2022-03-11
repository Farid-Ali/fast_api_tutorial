from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash password (user password)
    hashed_password = utils.convert_to_hash(user.password)
    
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    #retrive the new user
    db.refresh(new_user)
    
    return new_user




@router.get("/{id}", response_model=schemas.UserResponse)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    return user
        