from fastapi import status, HTTPException, Depends, APIRouter
import schema.user_schema as user_schema
import models.user_model as user_model
from sqlalchemy.orm import Session
from database.database import get_db
import utils.utils as utils

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOut)
def create_user(user: user_schema.UserBase, db : Session = Depends(get_db)):
    #Hast the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = user_model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=user_schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} doesnot exists")
    
    return user