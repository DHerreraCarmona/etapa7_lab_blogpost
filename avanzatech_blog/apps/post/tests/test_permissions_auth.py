import pytest
from apps.post.models import Post, Like, Comment
from apps.post.serializers import PostSerializer
from apps.post.tests.test_init import CreateUsers,Create_Posts,LoginUser1

#Test Auth user permissions ***************************************************************************************************************
@pytest.mark.permissions_auth
def test_auth_user_post_permissions(LoginUser1,Create_Posts):
    response,client,user1 = LoginUser1
    post_public_id,post_auth_id,post_team_id,post_teamread_id,post_priv_id = Create_Posts

    #Test post list, create post --------------------------------------------------------------------------------------------
    response = client.get("/post/")                                                 #Test post list
    assert response.status_code == 200
    db_public_post_serialized = PostSerializer(Post.objects.get(id=post_public_id)).data
    db_auth_post_serialized = PostSerializer(Post.objects.get(id=post_auth_id)).data
    assert response.data["results"][0] == db_public_post_serialized                 #Get public == DB
    assert response.data["results"][1] == db_auth_post_serialized                   #Get auth == DB
    assert len(response.data["results"]) == 2                                       #Only returns public & auth posts

    response = client.post("/post/create/", {"author":user1,                        #Test Create
                                             "title":"Test Title create",
                                             "content":"Test Content"})
    assert response.status_code == 201                                              #Test status created
    assert Post.objects.filter(title="Test Title create").exists()                  #Test created in db   

    #Test detail post view -------------------------------------------------------------------------------------------------
    response = client.get(f"/post/{post_public_id}/")                               #Test detail public post
    assert response.status_code == 200                                   
    assert response.data == db_public_post_serialized

    response = client.get(f"/post/{post_auth_id}/")                                 #Test detail auth post
    assert response.status_code == 200                                   
    assert response.data == db_auth_post_serialized

    response = client.get(f"/post/{post_team_id}/")                                 #Test detail team post no access 404
    assert response.status_code == 404  

    response = client.get(f"/post/{post_priv_id}/")                                 #Test detail private post no access 404
    assert response.status_code == 404     

    #Test edit ------------------------------------------------------------------------------------------------------------
    response = client.patch(f"/blog/{post_public_id}/",                             #Test edit post by owner
                            {"title":"Title 1 modified",
                             "content":"Test Content modified"}) 
    assert response.status_code == 200                                              #Test status modified
    assert Post.objects.filter(title="Title 1 modified").exists()                   #Test exist in db  

    response = client.patch(f"/blog/{post_auth_id}/")                               #Test edit auth post no access 404
    assert response.status_code == 404   

    response = client.patch(f"/blog/{post_team_id}/")                               #Test edit team post no access 404
    assert response.status_code == 404   

    response = client.patch(f"/blog/{post_priv_id}/")                               #Test edit priv post no access 404
    assert response.status_code == 404   

    #Test give-like action ------------------------------------------------------------------------------------------------
    response = client.post(f"/post/{post_public_id}/give-like/")                    #Test public post give like 200
    assert response.status_code == 200 
    assert Like.objects.filter(author=user1).filter(post=post_public_id).exists()    

    response = client.post(f"/post/{post_auth_id}/give-like/")                      #Test auth post give like 200
    assert response.status_code == 200
    assert Like.objects.filter(author=user1).filter(post=post_auth_id).exists()     

    response = client.post(f"/post/{post_team_id}/give-like/")                      #Test team post give like 403
    assert response.status_code == 403
    assert not Like.objects.filter(author=user1).filter(post=post_team_id).exists() 

    response = client.post(f"/post/{post_priv_id}/give-like/")                      #Test priv post give like 403
    assert response.status_code == 403
    assert not Like.objects.filter(author=user1).filter(post=post_priv_id).exists() 

    #Test write-comment action ---------------------------------------------------------------------------------------------
    response = client.post(f"/post/{post_public_id}/write-comment/",                #Test public post write comment 201
                            {"author":user1, "post_id":post_public_id,
                            "content":"Test Comment"})                                     
    assert response.status_code == 201 
    assert  Comment.objects.filter(author=user1).filter(post=post_public_id).exists()      


    response = client.post(f"/post/{post_auth_id}/write-comment/",                   #Test auth post write comment 201
                            {"author":user1, "post_id":post_auth_id,
                            "content":"Test Comment"})                   
    assert response.status_code == 201
    assert Comment.objects.filter(author=user1).filter(post=post_auth_id).exists()   

    response = client.post(f"/post/{post_team_id}/write-comment/",                  #Test team post write comment 403
                            {"author":user1, 
                            "post_id":post_team_id,"content":"Test Comment"})                   
    assert response.status_code == 403  
    assert not Comment.objects.filter(author=user1).filter(post=post_team_id).exists()    

    response = client.post(f"/post/{post_priv_id}/write-comment/",                  #Test priv post write comment 403
                             {"author":user1, 
                            "post_id":post_priv_id,"content":"Test Comment"})                   
    assert response.status_code == 403  
    assert not Comment.objects.filter(author=user1).filter(post=post_priv_id).exists()