from fastapi import Depends, Response, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, OAuth2

router = APIRouter(
  tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
  
  #verify if the user exists in the db
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
  
  #verify if user provided password and password in the db match
  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
  
  #create token
  access_token = OAuth2.create_access_token(data={"user_id": user.id})
  
  #return token
  
  return { "access_token": access_token, "token_type": "bearer" }