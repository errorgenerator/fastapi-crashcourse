from datetime import datetime
from fastapi import status
from starlette.responses import Response
from fastapi_app import app
from blogpost_dict import blogposts

from models import Blogpost, UpdateBody

@app.get("/posts")
def getAllPosts():
    """
    Returns a list with ALL BlogPosts.
    Accepts a GET-Request and returns application/json
    """
    return blogposts


@app.get("/posts/{id}")
def getPostById(id: int, response: Response):
    """
    Returns the Post with the specified ID.
    The Path-Parameter is id.
    so /posts/1 will return the Post with id==1.
    Accepts a GET-Request and returns application/json
    If no Post with the specified ID can be found
    it will return a status 404
    """
    for post in blogposts:
        postId = post["id"]
        if postId != None and postId == id:
            return post
    response.status_code = status.HTTP_404_NOT_FOUND # if the post is not in the "database"
    return { "message": "Not found!" }

@app.post("/posts")
def createPost(body: Blogpost, response: Response):
    """
    Adds a new Blogpost to the "database"
    Accepts a POST-Request with a JSON-Body
    containing a Blogpost
    """
    id = len(blogposts) + 1

    object_to_insert = {
        "id": id,
        "created": datetime.strftime(datetime.now(), "%d-%m-%y"),
        "updated": None,
        "author": body.author,
        "content": body.content
    }

    blogposts.append(object_to_insert)
    response.status_code = status.HTTP_201_CREATED
    return object_to_insert


@app.put("/posts/{id}")
def updatePost(id: int, body: UpdateBody, response: Response):
    """
    Endpoint for updating a Blogpost.
    This will change the "author" and "content" fields
    of a blogpost with the specified ID.
    If successful, it returns the updated Blogpost.
    If no Blogpost with the specified ID can be found,
    it returns a 404 Not Found.
    """
    for post in blogposts:
        postId = post["id"]
        if postId != None and postId == id:
            blogposts.remove(post)
            # modify in place
            post = {
                "id": post["id"],
                "created": post["created"],
                "updated": datetime.strftime(datetime.now(), "%d-%m-%y"),
                "content": body.content,
                "author": body.author,
            }
            blogposts.append(post)
            response.status_code = status.HTTP_202_ACCEPTED
            return post
    response.status_code = status.HTTP_404_NOT_FOUND
    return { "message": "Not Found!" }

@app.delete("/posts/{id}")
def deletePost(id: int, response: Response):
    for post in blogposts:
        postId = post["id"]
        if postId != None and postId == id:
            blogposts.remove(post)
            response.status_code = status.HTTP_200_OK
            return post
    response.status_code = status.HTTP_404_NOT_FOUND
    return { "message": "Not Found!" }
