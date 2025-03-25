import pytest
from apps.post.models import Post, Like, Comment
from apps.post.serializers import PostSerializer
from apps.post.tests.test_init import CreateUsers,Create_Posts,LoginUser3

#Test Team user permissions *************************************************************************************************************
@pytest.mark.permissions_team
def test_team_user_post_permissions(LoginUser3,Create_Posts):
    response,client,user3= LoginUser3
    post_public_id,post_auth_id,post_team_id,post_teamedit_id,post_priv_id = Create_Posts

    #Test post list  --------------------------------------------------------------------------------------------------------
    response = client.get("/post/")                                                 #Test post list
    assert response.status_code == 200
    db_public_post_serialized = PostSerializer(Post.objects.get(id=post_public_id)).data
    db_auth_post_serialized = PostSerializer(Post.objects.get(id=post_auth_id)).data
    db_team_post_serialized = PostSerializer(Post.objects.get(id=post_team_id)).data
    db_teamread_post_serialized = PostSerializer(Post.objects.get(id=post_teamedit_id)).data

    assert response.data["results"][0] == db_public_post_serialized                 #Get public == DB
    assert response.data["results"][1] == db_auth_post_serialized                   #Get auth == DB
    assert response.data["results"][2] == db_team_post_serialized                   #Get teamread == DB
    assert response.data["results"][3] == db_teamread_post_serialized               #Get teamedit == DB
    assert len(response.data["results"]) == 4                                       #Only returns public,auth & team posts

    #Test detail post view -------------------------------------------------------------------------------------------------
    response = client.get(f"/post/{post_public_id}/")                               #Test detail public post
    assert response.status_code == 200                                   
    assert response.data == db_public_post_serialized

    response = client.get(f"/post/{post_auth_id}/")                                 #Test detail auth post
    assert response.status_code == 200                                   
    assert response.data == db_auth_post_serialized

    response = client.get(f"/post/{post_team_id}/")                                 #Test detail team post
    assert response.status_code == 200  

    response = client.get(f"/post/{post_priv_id}/")                                 #Test detail private post no access 404
    assert response.status_code == 404

    #Test edit ------------------------------------------------------------------------------------------------------------
    response = client.patch(f"/blog/{post_public_id}/",                             #Test edit public post no owner
                            {"title":"Title 1 modified",
                             "content":"Test Content modified"}) 
    assert response.status_code == 404                                              
    assert not Post.objects.filter(title="Title 1 modified").exists()                

    response = client.patch(f"/blog/{post_team_id}/",                               #Test edit team read post no access 404
                            {"title":"Test title 3 team read modified",
                            "content":"Test Content modified"})                      
    assert response.status_code == 404
    assert not Post.objects.filter(title="Test title 3 team read modified").exists()

    response = client.patch(f"/blog/{post_teamedit_id}/",                            #Test edit team-edit post
                            {"title":"Test title 3 team read modified",
                            "content":"Test Content modified"})                      
    assert response.status_code == 200
    assert Post.objects.filter(title="Test title 3 team read modified").exists()    
  
    #Test give-like action ------------------------------------------------------------------------------------------------
    response = client.post(f"/post/{post_team_id}/give-like/")                      #Test team post give like
    assert response.status_code == 200
    assert  Like.objects.filter(author=user3).filter(post=post_team_id).exists()

    response = client.post(f"/post/{post_teamedit_id}/give-like/")                  #Test team-edit post give like
    assert response.status_code == 200
    assert Like.objects.filter(author=user3).filter(post=post_team_id).exists() 

    #Test write-comment action ---------------------------------------------------------------------------------------------
    response = client.post(f"/post/{post_team_id}/write-comment/",                  #Test team post write comment
                             {"author":user3, 
                            "post_id":post_team_id,"content":"Test Comment"})                   
    assert response.status_code == 201  
    assert Comment.objects.filter(author=user3).filter(post=post_team_id).exists()    

    
    response = client.post(f"/post/{post_teamedit_id}/write-comment/",              #Test team-edit post write comment
                             {"author":user3, 
                            "post_id":post_teamedit_id,"content":"Test Comment"})                   
    assert response.status_code == 201  
    assert Comment.objects.filter(author=user3).filter(post=post_teamedit_id).exists()      
    

