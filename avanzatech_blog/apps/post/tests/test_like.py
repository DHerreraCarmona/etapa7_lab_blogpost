import pytest

from apps.post.serializers import ShortLikeSerializer,DetailLikeSerializer
from apps.post.models import Post,Like
from test_init import CreateUser, LoginUser, Create_Post, Create_Like_Post_Login

#Create comment in DataBase -------------------------------------------------------------------------------------------------------------------------
@pytest.mark.like_view
def test_create_Like_db(Create_Post):
    client,post_id,user1 = Create_Post
    Like.objects.create(author=user1, post_id=post_id)
    assert Like.objects.filter(author=user1).filter(post_id=post_id).exists()  #Test created in db

#Test Comment List, filter by Post & User View ------------------------------------------------------------------------------------------------------
@pytest.mark.like_view
def test_like_list_view(Create_Like_Post_Login):
    client,response,post_id,_ = Create_Like_Post_Login

    response = client.get(f"/likes/")
    db_comment_serialized = DetailLikeSerializer(Like.objects.get(post=post_id)).data
    assert response.status_code == 200                                   
    assert response.data["results"][0] == db_comment_serialized                    #Test retrieve = db

@pytest.mark.like_view
def test_like_get_by_post(Create_Like_Post_Login):
    client,response,post_id,_ = Create_Like_Post_Login

    response = client.get(f"/likes/post/{post_id}/")
    db_like_serialized = DetailLikeSerializer(Like.objects.get(post=post_id)).data
    assert response.status_code == 200                             
    assert response.data["results"][0] == db_like_serialized                       #Test retrieve = db

@pytest.mark.like_view
def test_like_get_by_author(Create_Like_Post_Login):
    client,response,post_id,user1 = Create_Like_Post_Login
    response = client.get(f"/likes/author/{user1.id}/")
    db_like_serialized = DetailLikeSerializer(Like.objects.get(author=user1.id)).data
    assert response.status_code == 200                                   
    assert response.data["results"][0] == db_like_serialized                       #Test retrieve = db

#Test Create,Patch,Delete,Retrieve Post Viewset -----------------------------------------------------------------------------------------------------
@pytest.mark.like_viewset
def test_like_retrieve_action(Create_Like_Post_Login):
    client,response,post_id,_ = Create_Like_Post_Login
    response = client.get(f"/post/{post_id}/likes/")
    db_like_serialized = ShortLikeSerializer(Like.objects.get(post=post_id)).data
    assert response.status_code == 200                                   
    assert response.data[0] == db_like_serialized                       #Test retrieve = db

@pytest.mark.like_viewset
def test_like_create_action(LoginUser,Create_Post):
    client,post_id,user1 = Create_Post
    response = client.post(f"/post/{post_id}/give-like/", {"author":user1, "post_id":post_id})
    assert response.status_code == 200                                          #Test status created
    assert Like.objects.filter(author=user1).filter(post_id=post_id).exists()   #Test created in db

@pytest.mark.like_viewset
def test_like_delete_action(LoginUser,Create_Post):
    client,post_id,user1 = Create_Post
    response = client.post(f"/post/{post_id}/give-like/", {"author":user1, "post_id":post_id})  #like
    response = client.post(f"/post/{post_id}/give-like/", {"author":user1, "post_id":post_id})  #dislike
    assert response.status_code == 200                                   #Test status created
    assert not Like.objects.filter(author=user1).filter(post_id=post_id).exists()   #Test created in db