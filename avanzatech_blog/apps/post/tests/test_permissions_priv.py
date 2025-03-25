import pytest
from apps.post.models import Post, Like, Comment
from apps.post.serializers import PostSerializer
from apps.post.tests.test_init import CreateUsers,Create_Posts,LoginUser4

#Test Team user permissions *************************************************************************************************************
@pytest.mark.permissions_priv
def test_user_priv_post_permissions(LoginUser4,Create_Posts):
    response,client,user4= LoginUser4
    post_public_id,post_auth_id,post_team_id,post_teamedit_id,post_priv_id = Create_Posts

    #Test post list  --------------------------------------------------------------------------------------------------------
    response = client.get("/post/")                                                 #Test post list
    assert response.status_code == 200
    db_public_post_serialized = PostSerializer(Post.objects.get(id=post_public_id)).data
    db_auth_post_serialized = PostSerializer(Post.objects.get(id=post_auth_id)).data
    db_team_post_serialized = PostSerializer(Post.objects.get(id=post_team_id)).data
    db_teamread_post_serialized = PostSerializer(Post.objects.get(id=post_teamedit_id)).data
    db_priv_post_serialized = PostSerializer(Post.objects.get(id=post_priv_id)).data

    assert response.data["results"][0] == db_public_post_serialized                 #Get public == DB
    assert response.data["results"][1] == db_auth_post_serialized                   #Get auth == DB
    assert response.data["results"][2] == db_priv_post_serialized                   #Get priv == DB
    assert len(response.data["results"]) == 3                                       #Only returns public, auth & priv posts

    #Test detail post view -------------------------------------------------------------------------------------------------                    
    response = client.get(f"/post/{post_priv_id}/")                                 #Test detail private post
    assert response.status_code == 200
    assert response.data == db_priv_post_serialized 

    #Test edit ------------------------------------------------------------------------------------------------------------
    response = client.patch(f"/blog/{post_priv_id}/",                               #Test edit priv post
                            {"title":"Test title 5 private modified",
                             "content":"Test Content modified"}) 
    assert response.status_code == 200                                             
    assert Post.objects.filter(title="Test title 5 private modified").exists()     

    #Test give-like action ------------------------------------------------------------------------------------------------
    response = client.post(f"/post/{post_priv_id}/give-like/")                      #Test priv post give like
    assert response.status_code == 200
    assert Like.objects.filter(author=user4).filter(post=post_priv_id).exists()

    #Test write-comment action ---------------------------------------------------------------------------------------------
    response = client.post(f"/post/{post_priv_id}/write-comment/",                  #Test priv post write comment
                             {"author":user4, 
                            "post_id":post_priv_id,"content":"Test Comment"})                   
    assert response.status_code == 201  
    assert Comment.objects.filter(author=user4).filter(post=post_priv_id).exists()    