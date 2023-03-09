from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CarPictureSchema(BaseModel):
    """Car Picture Schema"""
    url: str = Field(title="", description="",)
    car_id: str = Field(title="", description="",)
    active: bool = Field(title="", description="",)

    class Config:
        """Config"""
        orm_mode = True
        schema_extra = {
            "example": {
                "url": "Picture URL for ad",
                "car_id": 1,
                "active": True
            }
        }


class CarPictureResponse(BaseModel):
    """Car picturу response schema"""
    id: int = Field(title="Id", description="")
    url: str = Field(title="", description="")
    active: bool = Field(title="", description="")

    class Config:
        """Config"""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "url": "Title for ad",
                "active": True
            }
        }
