import pytest
from jose import jwt
from app import schemas
from app.config import settings



# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World!'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", json={"email" : "hello123@gmail.com","password" : "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201, res.text
    #assert res.status_code == 200, res.text
    data = res.json()
    assert data["email"] == "hello123@gmail.com"
    assert "id" in data
    user_id = data["id"]

    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["email"] == "hello123@gmail.com"
    assert data["id"] == user_id

def test_login_user(test_user,client):
    res = client.post(
        "/login", data={"username": test_user['email'],"password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password,status_code",[
    ("worngemail@gmail.com","password123",403),
    ("hello123@gmail.com","wrongpass",403),
    ("worngemail@gmail.com","wrongpass",403),
    (None,"password123",422),
    ("hello123@gmail.com",None,422)
])
def test_incorrect_login(test_user,client,email,password,status_code):
    # res = client.post(
    #     "/login", data={"username": test_user['email'],"password": "wrongpass"}
    # )
    res = client.post(
        "/login", data={"username": email,"password": password}
    )
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'