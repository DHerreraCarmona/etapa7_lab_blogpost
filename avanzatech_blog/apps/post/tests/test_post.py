import pytest

from apps.post.serializers import PostSerializer
from apps.post.models import Post
from test_init import CreateUser,LoginUser, LoginPost

#Create Post in DataBase -------------------------------------------------------------------------------------------------------------------------
@pytest.mark.post_view
def test_create_post(CreateUser):
    client,user1 = CreateUser
    Post.objects.create(author=user1, title="Test Title 1",content="Test Content")
    assert Post.objects.filter(title="Test Title 1").exists()

#Test Create,Patch,Delete,Retrieve Post View -----------------------------------------------------------------------------------------------------
@pytest.mark.post_view
def test_post_create_view(CreateUser,LoginUser):
    client,user1 = CreateUser
    response = client.post("/post/create/", {"author":user1, "title":"Test Title 2","content":"Test Content"})
    assert response.status_code == 201                          #Test status created
    assert Post.objects.filter(title="Test Title 2").exists()   #Test created in db

@pytest.mark.post_view
def test_post_list_view(LoginPost,LoginUser):
    response,client,post_id,_ = LoginPost
    response = client.get("/post/")
    db_comment_serialized = PostSerializer(Post.objects.get(id=post_id)).data
    assert response.status_code == 200                                   
    assert response.data["results"][0] == db_comment_serialized                       #Test retrieve = db

@pytest.mark.post_view
def test_post_patch_view(LoginPost):
    response,client,post_id,_ = LoginPost
    response = client.patch(f"/blog/{post_id}/", {"title":"Test Title 2 modified","content":"Test Content modified"})
    assert response.status_code == 200                                   #Test status modified
    assert Post.objects.filter(title="Test Title 2 modified").exists()   #Test exist in db

@pytest.mark.post_view
def test_post_delete_view(LoginPost):
    response,client,post_id,_ = LoginPost
    response = client.delete(f"/blog/{post_id}/")
    assert response.status_code == 204                              #Test status no content
    assert not Post.objects.filter(title="Test Title 2").exists()   #Test deleted in db

#Test Post Detail & delete Viewset -----------------------------------------------------------------------------------------------------
@pytest.mark.post_viewset
def test_post_detail_viewset(LoginPost):
    response,client,post_id,_ = LoginPost
    response = client.get(f"/post/{post_id}/")
    db_post_serialized = PostSerializer(Post.objects.get(id=post_id)).data
    assert response.status_code == 200                    #Test status modified
    assert response.data == db_post_serialized

@pytest.mark.post_viewset
def test_post_detail_viewset(LoginPost):
    response,client,post_id,user1 = LoginPost
    response = client.delete(f"/post/{post_id}/")
    assert not Post.objects.filter(id=post_id).exists()   #Test deleted in db

