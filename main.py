from fastapi import FastAPI
# import models.post_model as post_model
# import models.user_model as user_model
# import models.vote_model as vote_model
# from database.database import engine
from routers import post, user, auth, vote
from config import Settings, settings
# Setting Up Cors (Cross Origin Resource Sharing)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*",
]
# * refer to all domains
# It is security best practice

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This creates the database tables
# post_model.Base.metadata.create_all(bind=engine)
# user_model.Base.metadata.create_all(bind=engine)
# vote_model.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastApi Sandeep"}