from pydantic import BaseModel

class Blogpost(BaseModel):
    """
    DTO (Data Transfer Object) for a Blogpost.
    The assignments for IDs is done solely by
    the service. The client does not have control
    over assigning IDs to keep the "database" consistent
    """
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
