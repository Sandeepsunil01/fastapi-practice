from fastapi import APIRouter,Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database.database import get_db
from models.user_model import User
from utils.utils import verify
import outh2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #Create a token and return it
    access_token = outh2.create_access_token(data={"user_id": user.id})
    
    return {
        "token": access_token,
        "token_type": "bearer"
    }