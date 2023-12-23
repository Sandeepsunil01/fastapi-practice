from database.database import Base
from sqlalchemy import Column, ForeignKey, Integer

class Votes(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("new_posts.id", ondelete="CASCADE"), primary_key=True)