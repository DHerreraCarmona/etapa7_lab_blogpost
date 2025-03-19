import pytest
from django.contrib.auth import get_user
from rest_framework.test import APIClient
from django.contrib.auth.models import AnonymousUser

from apps.post.serializers import PostSerializer
from apps.post.models import Post,Comment, Like
from apps.user.views import login_view
from test_init import CreateUsers

#Create user in DataBase -------------------------------------------------------------------------------------------------------------------------
def test_create_post(CreateUsers):
    client,user1,_,_,_,_ = CreateUsers
    Post.objects.create(author=user1, title="Test Title 1",content="Test Content")
    assert Post.objects.filter(title="Test Title 1").exists()

#Test Create,Patch,Delete,Retrieve Post View -----------------------------------------------------------------------------------------------------
@pytest.fixture
def LoginUser1(CreateUsers):
    client,user1,_,_,_,_ = CreateUsers
    response = client.post("/user/api-auth/login/", {"username": "user1@test.com", "password": "test_password"})

@pytest.fixture
def LoginPost(CreateUsers,LoginUser1):
    client,user1,_,_,_,_ = CreateUsers
    response = client.post("/post/create/", {"author":user1, "title":"Test Title 2","content":"Test Content"})
    return response

def test_post_create_view(CreateUsers,LoginUser1):
    client,user1,_,_,_,_ = CreateUsers

    response = client.post("/post/create/", {"author":user1, "title":"Test Title 2","content":"Test Content"})
    assert response.status_code == 201                          #Test status created
    assert Post.objects.filter(title="Test Title 2").exists()   #Test created in db

def test_post_patch_view(CreateUsers,LoginPost):
    client,_,_,_,_,_ = CreateUsers
    response = LoginPost
    post_id = response.data.get("id")
    response = client.patch(f"/blog/{post_id}/", {"title":"Test Title 2 modified","content":"Test Content modified"})
    assert response.status_code == 200                                   #Test status modified
    assert Post.objects.filter(title="Test Title 2 modified").exists()   #Test exist in db

def test_post_retrieve_view(CreateUsers,LoginPost):
    client,user1,_,_,_,_ = CreateUsers
    response = LoginPost
    post_id = response.data.get("id")
    response = client.get(f"/post/{post_id}/")
    db_post_serialized = PostSerializer(Post.objects.get(id=post_id)).data

    assert response.status_code == 200                                   #Test status modified
    assert response.data == db_post_serialized

def test_post_delete_view(CreateUsers,LoginPost):
    client,_,_,_,_,_ = CreateUsers
    response = LoginPost
    post_id = response.data.get("id")
    response = client.delete(f"/blog/{post_id}/")
    assert response.status_code == 204                              #Test status no content
    assert not Post.objects.filter(title="Test Title 2").exists()   #Test deleted in db
"""

#Create Login & Unlog User Views--------------------------------------------------------------------------------------------------------------------------


def test_login_view(ClientUser):
    client, user = ClientUser
    response = client.post("/user/api-auth/login/", {"username": "testuser@test.com", "password": "test_password"},follow=True)
    authenticated_user = get_user(client)              

    assert response.status_code == 200                #Test Redirect to post page
    assert response.request["PATH_INFO"] == "/post/" 
    assert authenticated_user.is_authenticated        #Test Auth
    assert authenticated_user.id == user.id
    assert "_auth_user_id" in client.session 

def test_login_view_fail(ClientUser):
    client, _ = ClientUser
    response = client.post("/user/api-auth/login/", {"username": "user", "password": "nopassword"},follow=True)
    unauthenticated_user = get_user(client)             

    assert response.status_code == 200                      #Test Redirect to login page
    assert isinstance(unauthenticated_user, AnonymousUser)  #Test Auth Fail 

def test_logout(ClientUser):
    client, _ = ClientUser
    response = client.post("/user/api-auth/login/", {"username": "testuser@test.com", "password": "test_password"},follow=True)
    assert "_auth_user_id" in client.session                        #Login First

    response = client.post("/user/api-auth/logout/", follow=True)   #Logout
    assert response.status_code == 200                              #Test Redirect
    assert "_auth_user_id" not in client.session                    #Test Unlog"""