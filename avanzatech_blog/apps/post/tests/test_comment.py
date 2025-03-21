import pytest

from apps.post.serializers import ShortCommentSerializer,DetailCommentSerializer
from apps.post.models import Post,Comment
from test_init import CreateUser,LoginUser, Create_Post, Create_Comment_Post_Login

#Create comment in DataBase -------------------------------------------------------------------------------------------------------------------------
@pytest.mark.comment_view
def test_create_comment_db(Create_Post):
    client,post_id,user1 = Create_Post
    Comment.objects.create(author=user1, post_id=post_id, content="Test Comment 1")
    assert Comment.objects.filter(content="Test Comment 1").exists()  #Test created in db

#Test Comment List, filter by Post & User View ------------------------------------------------------------------------------------------------------
@pytest.mark.comment_view
def test_comment_list_view(Create_Comment_Post_Login):
    client,response,post_id,_ = Create_Comment_Post_Login
    response = client.get(f"/comments/")
    db_comment_serialized = DetailCommentSerializer(Comment.objects.get(post=post_id)).data
    assert response.status_code == 200                                   
    assert response.data["results"][0] == db_comment_serialized                       #Test retrieve = db

@pytest.mark.comment_view
def test_comment_get_by_post(Create_Comment_Post_Login):
    client,response,post_id,_ = Create_Comment_Post_Login
    response = client.get(f"/comments/post/{post_id}/")
    db_comment_serialized = DetailCommentSerializer(Comment.objects.get(post=post_id)).data
    assert response.status_code == 200                                   
    assert response.data["results"][0] == db_comment_serialized                       #Test retrieve = db

@pytest.mark.comment_view
def test_comment_get_by_author(Create_Comment_Post_Login):
    client,response,post_id,user1 = Create_Comment_Post_Login
    response = client.get(f"/comments/author/{user1.id}/")
    db_comment_serialized = DetailCommentSerializer(Comment.objects.get(author=user1.id)).data
    assert response.status_code == 200                                   
    assert response.data["results"][0] == db_comment_serialized                       #Test retrieve = db

#Test Create,Patch,Delete,Retrieve Post Viewset -----------------------------------------------------------------------------------------------------
@pytest.mark.comment_viewset
def test_comment_create_action(LoginUser,Create_Post):
    client,post_id,user1 = Create_Post
    response = client.post(f"/post/{post_id}/write-comment/", {"author":user1, "post_id":post_id,"content":"Test Comment 2"})
    assert response.status_code == 201                                 #Test status created
    assert Comment.objects.filter(content="Test Comment 2").exists()   #Test created in db

@pytest.mark.comment_viewset
def test_comment_list_viewset(Create_Comment_Post_Login):
    client,response,post_id,_ = Create_Comment_Post_Login
    response = client.get(f"/post/{post_id}/comments/")
    db_comment_serialized = ShortCommentSerializer(Comment.objects.get(post=post_id)).data
    assert response.status_code == 200                                   
    assert response.data[0] == db_comment_serialized                       #Test retrieve = db

@pytest.mark.comment_viewset
def test_detail_comment_get_viewset(Create_Comment_Post_Login):
    client,response,post_id,_ = Create_Comment_Post_Login
    response = client.get(f"/post/{post_id}/comments/1/")
    db_comment_serialized = ShortCommentSerializer(Comment.objects.get(post=post_id)).data
    assert response.status_code == 200                                   
    assert response.data == db_comment_serialized                       #Test retrieve = db

@pytest.mark.comment_viewset
def test_comment_patch_viewset(Create_Comment_Post_Login):
    client,response,post_id,user1 = Create_Comment_Post_Login
    response = client.patch(f"/post/{post_id}/comments/1/", {"author":user1, "post_id":post_id,"content":"Test Comment user1 modified"})
    assert response.status_code == 201                                              #Test status modified
    assert Comment.objects.filter(content="Test Comment user1 modified").exists()   #Test exist in db

@pytest.mark.comment_viewset
def test_comment_delete_viewset(Create_Comment_Post_Login):
    client,response,post_id,user1 = Create_Comment_Post_Login
    response = client.delete(f"/post/{post_id}/comments/1/")  
    assert response.status_code == 204                                         #Test status no content
    assert not Comment.objects.filter(content="Test Comment user1").exists()   #Test not exist in db