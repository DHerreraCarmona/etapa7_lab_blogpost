import pytest
from rest_framework.test import APIClient
from apps.user.models import CustomUser,Group
from apps.post.models import Post, Permissions
from apps.post.serializers import PostSerializer


@pytest.fixture
def CreateUsers(db):
    group1 = Group.objects.create(name="test1")
    group2 =Group.objects.create(name="test2")
    client=APIClient()
    user1 = CustomUser.objects.create_user(email="user1@test.com",
                            username="user1",
                            password="test_password",
                            is_active=1,
                            is_staff=0,
                            group=group1)
    user2 = CustomUser.objects.create_user(email="user2@test.com",
                            username="user2",
                            password="test_password",
                            is_active=1,
                            is_staff=0,
                            group=group2)
    user3 = CustomUser.objects.create_user(email="user3@test.com",
                            username="user3",
                            password="test_password",
                            is_active=1,
                            is_staff=0,
                            group=group1)
    user4 = CustomUser.objects.create_user(email="user4@test.com",
                            username="user4",
                            password="test_password",
                            is_active=1,
                            is_staff=0,
                            group=group2)
    user5 = CustomUser.objects.create_user(email="user5@test.com",
                            username="user5",
                            password="test_password",
                            is_active=1,
                            is_staff=0,
                            group=None)
    return client,user1,user2,user3,user4,user5

@pytest.fixture
def Create_Posts(db,CreateUsers):
    client,user1,user2,user3,user4,user5 = CreateUsers
    post_id_public=Post.objects.create(author=user1,
                                title="Test title 1public",
                                content="testing integration among models, views and permission",
                                public=Permissions.READONLY,
                                authenticated=Permissions.READONLY,
                                team=Permissions.READONLY,
                                owner=Permissions.READEDIT).id
    post_id_auth=Post.objects.create(author=user2,
                                title="Test title 2 auth",
                                content="testing integration among models, views and permission",
                                public=Permissions.HIDDEN,
                                authenticated=Permissions.READONLY,
                                team=Permissions.READONLY,
                                owner=Permissions.READEDIT).id
    post_id_team=Post.objects.create(author=user1,
                                title="Test title 3 team read",
                                content="testing integration among models, views and permission",
                                public=Permissions.HIDDEN,
                                authenticated=Permissions.HIDDEN,
                                team=Permissions.READONLY,
                                owner=Permissions.READEDIT).id
    post_id_team_edit=Post.objects.create(author=user1,
                                title="Test title 4 team edit",
                                content="testing integration among models, views and permission",
                                public=Permissions.HIDDEN,
                                authenticated=Permissions.HIDDEN,
                                team=Permissions.READEDIT,
                                owner=Permissions.READEDIT).id
    post_id_private=Post.objects.create(author=user1,
                                title="Test title 5 private",
                                content="testing integration among models, views and permission",
                                public=Permissions.HIDDEN,
                                authenticated=Permissions.HIDDEN,
                                team=Permissions.HIDDEN,
                                owner=Permissions.READEDIT).id
    return post_id_public, post_id_auth, post_id_team, post_id_team_edit, post_id_private  

@pytest.fixture
def LoginUser1(CreateUsers):
    client,_,_,_,_,_ = CreateUsers
    response = client.post("/user/api-auth/login/", {"username": "user1@test.com", "password": "test_password"})
    return response, client

@pytest.fixture
def LoginUser2(CreateUsers):
    client,_,_,_,_,_ = CreateUsers
    response = client.post("/user/api-auth/login/", {"username": "user2@test.com", "password": "test_password"})
    return response, client

@pytest.fixture
def LoginUser3(CreateUsers):
    client,_,_,_,_,_ = CreateUsers
    response = client.post("/user/api-auth/login/", {"username": "user3@test.com", "password": "test_password"})
    return response, client

@pytest.fixture
def LoginUser4(CreateUsers):
    client,_,_,_,_,_ = CreateUsers
    response = client.post("/user/api-auth/login/", {"username": "user4@test.com", "password": "test_password"})
    return response, client

@pytest.fixture
def LoginUser5(CreateUsers):
    client,_,_,_,_,_ = CreateUsers
    response = client.post("/user/api-auth/login/", {"username": "user5@test.com", "password": "test_password"})
    return response, client

@pytest.mark.permissions
def test_post_create_view(LoginUser1,Create_Posts):
    response,client = LoginUser1
    post_id,_,_,_,_ = Create_Posts
    response = client.get("/post/")
    db_comment_serialized = PostSerializer(Post.objects.get(id=post_id)).data
    assert response.status_code == 200                                   
    assert response.data["results"][0] == db_comment_serialized 
"""
@pytest.fixture
def LoginPost(CreateUsers,LoginUser1):
    client,user1 = CreateUsers
    response = client.post("/post/create/", {"author":user1, "title":"Test Title 2","content":"Test Content"})
    post_id = response.data.get("id")
    return response,client,post_id,user1

@pytest.fixture
def Create_Post(CreateUsers):
    client,user1  = CreateUsers
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
"""