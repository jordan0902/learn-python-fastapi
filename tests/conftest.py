from turtle import title
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
from app.database import get_db,Base
from app.main import app
from app.oauth2 import create_access_token
from app import models


#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Zmj413902:)@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@\
{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

#Base.metadata.create_all(bind=engine)

# Dependency
# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

#client = TestClient(app)
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    #run the code before running the testClient
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    #run the code after running the testClient

@pytest.fixture
def test_user(client):
    user_data = {
        "email" : "hello123@gmail.com",
        "password" : "password123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201, res.text
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {
        "email" : "hello1234@gmail.com",
        "password" : "password123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201, res.text
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers ={
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data = [{
        "title": "this is first post",
        "content": "1st content",
        "owner_id": test_user['id']
    },{
        "title": "this is 2nd post",
        "content": "2nd content",
        "owner_id": test_user['id']
    },{
        "title": "this is 3rd post",
        "content": "3rd content",
        "owner_id": test_user['id']
    },{
        "title": "this is 4th post",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(posts):
        return models.Post(**posts)

    post_map = map(create_post_model, posts_data)

    posts_list = list(post_map)
    session.add_all(posts_list)
    # session.add_all([models.Post(title = "this is first post", content = "1st content",
    #                 owner_id = test_user['id']),
    #                 models.Post(title = "this is 2nd post", content = "2nd content",
    #                 owner_id = test_user['id']),
    #                 models.Post(title = "this is 3nd post", content = "3nd content",
    #                 owner_id = test_user['id'])])
    session.commit()
    posts = session.query(models.Post).all()
    
    return posts