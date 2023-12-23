from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
import schema.post_schema as post_schema
from sqlalchemy.orm import Session
from database.database import get_db
import utils.utils as utils
import models.post_model as post_model
import models.vote_model as vote_model
import outh2
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[post_schema.Post])
# @router.get('/')
def get_posts(db:Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(post_model.Post).filter(post_model.Post.user_id == current_user.id).filter(post_model.Post.title.contains(search)).limit(limit).offset(skip).all() # type: ignore
    
    # posts = db.query(post_model.Post, func.count(vote_model.Votes.post_id).label("votes")).join(vote_model.Votes, vote_model.Votes.post_id == post_model.Post.id, isouter=True).group_by(post_model.Post.id).filter(post_model.Post.user_id == current_user.id).filter(post_model.Post.title.contains(search)).limit(limit).offset(skip).all() # type: ignore
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=post_schema.Post)
def create_posts(post: post_schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING  * """, (post.title, post.content, post.published),)
    # # conn.commit()
    # post_dict = post.dict()

    new_post = post_model.Post(user_id=current_user.id, **post.dict()) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.post("/{id}", status_code=status.HTTP_200_OK, response_model=post_schema.Post)
def get_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    post = db.query(post_model.Post, func.count(vote_model.Votes.post_id).label("votes")).join(vote_model.Votes, vote_model.Votes.post_id == post_model.Post.id, isouter=True).group_by(post_model.Post.id).filter(post_model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.user_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested actions")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    post_query = db.query(post_model.Post).filter(post_model.Post.id == id)
    post = post_query.first() 
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists")
    if post.user_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested actions")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=post_schema.Post)
def update_post(id: int, post: post_schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    post_query = db.query(post_model.Post).filter(post_model.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id}, does not exists")
    
    if updated_post.id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested actions")
    
    post_query.update(post.dict(), synchronize_session=False) # type: ignore
    db.commit()
    return post_query.first