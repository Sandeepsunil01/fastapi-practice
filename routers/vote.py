from fastapi import APIRouter,Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database.database import get_db
import outh2
from schema.vote_schema import Vote
from models.vote_model import Votes
from models.post_model import Post

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    post = db.query = db.query(Post).filter(Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exists")
    
    vote_query = db.query(Votes).filter(Votes.post_id == vote.post_id, Votes.user_id == current_user.id) # type: ignore
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}") # type: ignore
        new_vote = Votes(post_id=vote.post_id, user_id=current_user.id) # type: ignore
        db.add(new_vote)
        db.commit()
        return {"message" : "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exists")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Deleted Vote"}
