import pytest
from rest_framework.test import APIClient
from apps.user.models import CustomUser,Group
from apps.post.models import Post

@pytest.fixture
def CreateUser(db):
    client=APIClient()
    user1 = CustomUser.objects.create_user(email="user1@test.com",
                            username="user1",
                            password="test_password",
                            is_active=1,
                            is_staff=0,
                            group=None)

    return client,user1

@pytest.fixture
def LoginUser1(CreateUser):
    client,user1 = CreateUser
    response = client.post("/user/api-auth/login/", {"username": "user1@test.com", "password": "test_password"})

@pytest.fixture
def LoginPost(CreateUser,LoginUser1):
    client,user1 = CreateUser
    response = client.post("/post/create/", {"author":user1, "title":"Test Title 2","content":"Test Content"})
    post_id = response.data.get("id")
    return response,client,post_id,user1

@pytest.fixture
def Create_Post(CreateUser):
    client,user1  = CreateUser
    Post.objects.create(author=user1, title="Test Title 1",content="Test Content")
    post_id = Post.objects.get(title="Test Title 1").id
    return client,post_id, user1

@pytest.fixture
def Create_Comment_Post_Login(LoginUser1,Create_Post):
    client,post_id,user1 = Create_Post
    response = client.post(f"/post/{post_id}/write-comment/", {"author":user1, "post_id":post_id,"content":"Test Comment user1"})
    return client,response,post_id,user1

@pytest.fixture
def Create_Like_Post_Login(LoginUser1,Create_Post):
    client,post_id,user1 = Create_Post
    response = client.post(f"/post/{post_id}/give-like/", {"author":user1, "post_id":post_id})
    return client,response,post_id,user1