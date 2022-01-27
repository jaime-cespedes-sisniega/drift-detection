from pydantic import BaseModel


class Health(BaseModel):
    """Health schema"""

    name: str
    api_version: str
