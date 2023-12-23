from jose import JWTError, jwt
from datetime import datetime, timedelta
from schema import token_schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database.database import get_db
from sqlalchemy.orm import Session
from models.user_model import User
from config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#Secret Key
#Algorithm
#Expiration Time

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({
        "exp": expire,
    })

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token: str, creadentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id  = payload.get("user_id")

        if id is None:
            raise creadentials_exception
        token_data = token_schema.TokenData(id=id)
        return token_data
    except JWTError:
        raise creadentials_exception
    
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could Not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.id).first()
    return user 