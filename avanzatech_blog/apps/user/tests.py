import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser

from apps.user.models import CustomUser,Group

#Create user in DataBase -------------------------------------------------------------------------------------------------------------------------
@pytest.mark.user
def test_create_Group(db):
    Group.objects.create(name="test_group")
    assert Group.objects.filter(name="test_group").exists()

@pytest.mark.user
def test_create_User(db):
    CustomUser.objects.create(email="testuser@test.com",
                            username="test_user",
                            password="test_password",
                            is_active=1,
                            is_staff=0,
                            group=None)
    assert CustomUser.objects.filter(email="testuser@test.com").exists()

@pytest.mark.user
def test_create_User_fail(db):
    CustomUser.objects.create(email="NoEmail",
                            username="test_user",
                            password="",
                            is_active=1,
                            is_staff=0,
                            group=None)
    assert not CustomUser.objects.filter(email="testuser@test.com").exists()

#Test resgister User View -----------------------------------------------------------------------------------------------------------------------------
@pytest.mark.user
def test_register_view(db):
    client=APIClient()
    response = client.post("/user/api/register/", {"email":"testuser@test.com","username": "test_user", "password": "test_password"},format="json")

    assert response.status_code == 201
    assert CustomUser.objects.filter(email="testuser@test.com").exists()

def test_register_view_fail(db):
    client=APIClient()
    response = client.post("/user/api/register/", {"email":"NoEmail","username": "", "password": "123"},format="json")
    
    assert response.status_code == 400
    assert not CustomUser.objects.filter(email="NoEmail").exists()

#Create Login & Unlog User Views--------------------------------------------------------------------------------------------------------------------------
@pytest.fixture
def ClientUser(db):
    client=APIClient()
    user=CustomUser.objects.create_user(email="testuser@test.com",
                                        username="user",
                                        password="test_password",
                                        is_active=1,
                                        is_staff=0,
                                        group=None)
    return client, user

@pytest.mark.user
def test_login_view(ClientUser):
    client, user = ClientUser
    response = client.post("/user/api-auth/login/", {"username": "testuser@test.com", "password": "test_password"},follow=True)
    authenticated_user = get_user(client)              

    assert response.status_code == 200                              #Test Redirect to post page
    assert response.request["PATH_INFO"] == "/post/" 
    assert authenticated_user.is_authenticated                      #Test Auth
    assert authenticated_user.id == user.id
    assert "_auth_user_id" in client.session 

@pytest.mark.user
def test_login_view_fail(ClientUser):
    client, _ = ClientUser
    response = client.post("/user/api-auth/login/", {"username": "user", "password": "nopassword"},follow=True)
    unauthenticated_user = get_user(client)             

    assert response.status_code == 200                              #Test Redirect to login page
    assert isinstance(unauthenticated_user, AnonymousUser)          #Test Auth Fail 

@pytest.mark.user
def test_logout(ClientUser):
    client, _ = ClientUser
    response = client.post("/user/api-auth/login/", {"username": "testuser@test.com", "password": "test_password"},follow=True)
    assert "_auth_user_id" in client.session                        #Login First

    response = client.post("/user/api-auth/logout/", follow=True)   #Logout
    assert response.status_code == 200                              #Test Redirect
    assert "_auth_user_id" not in client.session                    #Test Unlog