import pytest
from apps.post.models import Post, Like, Comment
from apps.post.serializers import PostSerializer
from apps.post.tests.test_init import CreateUsers,Create_Posts,LoginAnon

#Test non-logged user permissions **********************************************************************************************************
@pytest.mark.permissions_anon
def test_anonymous_user_post_permissions(LoginAnon,Create_Posts):
    client = LoginAnon
    post_public_id,post_auth_id,post_team_id,post_teamread_id,post_priv_id  = Create_Posts

    #Test post list, deteail post, edit post, create post -----------------------------------------------------------------
    response = client.get("/post/")                                                 #Test post list
    db_post_serialized = PostSerializer(Post.objects.get(id=post_public_id)).data
    assert response.status_code == 200                                   
    assert response.data["results"][0] == db_post_serialized                        #Get == DB
    assert len(response.data["results"]) == 1                                       #Only returns public post

    response = client.get(f"/post/{post_public_id}/")                               #Test detail post
    assert response.status_code == 200                                   
    assert response.data == db_post_serialized                                      #Get == DB

    response = client.get(f"/post/{post_auth_id}/")                                 #Test detail auth post no access 404
    assert response.status_code == 404     

    response = client.get(f"/blog/{post_auth_id}/")                                 #Test edit auth post no access 404
    assert response.status_code == 404   

    response = client.get(f"/post/create/")                                         #Test create post forbidden 403
    assert response.status_code == 403                            

    #Test give-like action -------------------------------------------------------------------------------------------------
    response = client.post(f"/post/{post_public_id}/give-like/")                     #Test public post give like 403
    assert response.status_code == 403
    assert not Like.objects.filter(post=post_public_id).exists()                     #Test not created in db  

    response = client.post(f"/post/{post_auth_id}/give-like/")                       #Test auth post give like 403
    assert response.status_code == 403  
    assert not Like.objects.filter(post=post_auth_id).exists()                       

    response = client.post(f"/post/{post_team_id}/give-like/")                       #Test team post give like 403
    assert response.status_code == 403
    assert not Like.objects.filter(post=post_team_id).exists() 

    response = client.post(f"/post/{post_priv_id}/give-like/")                       #Test priv post give like 403
    assert response.status_code == 403
    assert not Like.objects.filter(post=post_priv_id).exists() 

    #Test write-comment action-----------------------------------------------------------------------------------------------
    response = client.post(f"/post/{post_public_id}/write-comment/")                #Test public post write comment 403     
    assert response.status_code == 403 
    assert not Comment.objects.filter(post=post_public_id).exists()      

    response = client.post(f"/post/{post_auth_id}/write-comment/")                  #Test auth post write comment 403
    assert response.status_code == 403  
    assert not Comment.objects.filter(post=post_auth_id).exists()   

    response = client.post(f"/post/{post_team_id}/write-comment/")                  #Test team post write comment 403
    assert response.status_code == 403  
    assert not Comment.objects.filter(post=post_team_id).exists()    

    response = client.post(f"/post/{post_priv_id}/write-comment/")                  #Test priv post write comment 403
    assert response.status_code == 403  
    assert not Comment.objects.filter(post=post_priv_id).exists()                     
