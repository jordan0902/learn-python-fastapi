from fastapi import APIRouter, Depends,status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model = schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    
    #username=
    #password=
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
   
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #create Token
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
 
    #return Token
    return {"access_token" : access_token, "token_type" : "bearer"}