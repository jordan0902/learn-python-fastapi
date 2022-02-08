from fastapi import FastAPI, Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip:int = 0, search:Optional[str] ="" ):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts
     

@router.get("/id_{id}",response_model=schemas.PostOut)
def get_postsbyid(id : int, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):#,response : Response):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s ;""", (str(id)))
    # post = find_post(id)
    # post = cursor.fetchone()
    #print(post)
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    #give bad page response to 404
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message":f"post with id: {id} does not exist!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist!")

    return  post

@router.get("/lastpost",response_model=schemas.Post)
def get_lastpost(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).order_by(desc(models.Post.id)).first()
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message":f"post with id: {id} does not exist!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Does not exist post yet, go to create one first!")

    return post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):
    #post_dict = post.dict()
    #post_dict["id"]  = randrange(0,10000)
    #return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
    #my_posts.append(post_dict)
    # cursor.execute(""" INSERT INTO posts (title, content,published) VALUES (%s,%s,%s) RETURNING * """,
    #     (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #print(**post.dict()) Arbitarary Keyword Arguments,
    #print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.put("/{id}",status_code=status.HTTP_205_RESET_CONTENT,response_model=schemas.Post)
def update_postsbyid(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    #update post
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *; """, 
    #     (post.title,post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist!")
        #user can only perform the action with his owne posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform action!")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_postsbyid(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #deleting post 
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *; """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist!")
    
    #user can only perform the action with his owne posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform action!")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)