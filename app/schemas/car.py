from uuid import UUID

from pydantic import BaseModel, Field


class CarSchema(BaseModel):
    """Car Schema"""
    title: str = Field(title="", description="",)
    content: str = Field(title="", description="",)

    class Config:
        """Config"""
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Name for Some car",
                "content": "Some Car Description",
            }
        }


class CarResponse(BaseModel):
    """Car response schema"""
    id: int = Field(title="Id", description="")
    title: str = Field(title="", description="")
    content: str = Field(title="", description="")

    class Config:
        """Config"""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Name for Some Stuff",
                "content": "Some Stuff Description",
            }
        }
