from datetime import datetime
from fastapi import FastAPI, status
from starlette.responses import Response
from pydantic import BaseModel

class Blogpost(BaseModel):
    """
    DTO (Data Transfer Object) for a Blogpost.
    The assignments for IDs is done solely by
    the service. The client does not have control
    over assigning IDs to keep the "database" consistent
    """
    created: str
    updated: str | None
    author: str
    content: str

class UpdateBody(BaseModel):
    """
    DTO (Data Transfore Object) for a Body for a PUT-Request.
    The client is only allowed to update the author
    and content of a Blogpost.
    ID, Created, Updated are being controlled by the service.
    """
    author: str
    content: str

# Here is our in-memory "database" of blogposts
blogposts = [
    {
        "id": 1,
        "created": "12-04-2024",
        "updated": None,
        "author": "errorgenerator",
        "content": "Lorem Ipsum"
    },
    {
        "id": 2,
        "created": "13-04-2024",
        "updated": None,
        "author": "errorgenerator",
        "content": "I am a Teapot"
    },
    {
        "id": 3,
        "created": "14-04-2024",
        "updated": None,
        "author": "errorgenerator",
        "content": "Lorem Ipsum 2"
    },
    {
        "id": 4,
        "created": "14-05-2024",
        "updated": None,
        "author": "errorgenerator",
        "content": "A million beers"
    }
]

# Create an instance of the Application Engine
# This will allow us to inject our Endpoint logic
# while the fastapi framework will take care of
# all the boring stuff, like interface binding
# concurrency, parsing, etc.
app = FastAPI()



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
        "created": body.created,
        "updated": body.updated,
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
            # modify in place
            post = {
                "id": post["id"],
                "created": post["created"],
                "updated": str(datetime.now),
                "content": body.content,
                "author": body.author,
            }
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
