from fastapi import FastAPI, Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas,database,models,oauth2

router = APIRouter(
    prefix= "/vote",
    tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db : Session = Depends(database.get_db), current_user : int =
Depends(oauth2.get_current_user)):

    #check if the post is exist 
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    found_post = post_query.first()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post does not exist!")

    #check the vote table if exist the vote from current user and the current post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    #dir = 1 : like it , dir = 0 : cancel like it.
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message" : "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist!")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message" : "successfully delete vote"}