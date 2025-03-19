import pytest
from rest_framework.test import APIClient
from apps.user.models import CustomUser,Group

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
