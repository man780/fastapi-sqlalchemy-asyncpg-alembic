from datetime import datetime
from uuid import UUID
from typing import List, TypeVar, Generic

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from app.schemas.car_picture import CarPictureResponse

T = TypeVar('T')

class CarSchema(BaseModel):
    """Car Schema"""
    title: str = Field(title="", description="",)
    content: str = Field(title="", description="",)

    class Config:
        """Config"""
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Title for Some ad",
                "content": "Some ad content",
            }
        }

class CarDetailResponse(BaseModel):
    """Car response schema"""
    id: int = Field(title="Id", description="")
    title: str = Field(title="", description="")
    content: str = Field(title="", description="")
    date: datetime = Field(title="", description="")
    hero_image: str = Field(title="", description="")
    url: str = Field(title="", description="")
    ad_id: UUID = Field(title="", description="")
    advert_id: UUID = Field(title="", description="")
    price: int = Field(title="", description="")
    make: str = Field(title="", description="")
    model: str = Field(title="", description="")
    color: str = Field(title="", description="")
    year: int = Field(title="", description="")
    city: str = Field(title="", description="")
    post_code: str = Field(title="", description="")
    mileage: int = Field(title="", description="")
    doors: int = Field(title="", description="")
    fuel: str = Field(title="", description="")
    transmission: str = Field(title="", description="")
    body_style: str = Field(title="", description="")
    engine_size: str = Field(title="", description="")
    seats: int = Field(title="", description="")
    car_type: str = Field(title="", description="")
    dealer_domain: str = Field(title="", description="")
    dealer_name: str = Field(title="", description="")
    priority: int = Field(title="", description="")
    seller_type: str = Field(title="", description="")
    vrm: str = Field(title="", description="")
    car_pictures: List["CarPictureResponse"]
    active: bool = Field(title="", description="")
    created: datetime = Field(title="", description="")

    class Config:
        """Config"""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Title for ad",
                "content": "Some ad content",
                "date": "some date"
            }
        }

class CarResponse(BaseModel):
    """Car response schema"""
    id: int = Field(title="Id", description="")
    title: str = Field(title="", description="")
    date: datetime = Field(title="", description="")
    hero_image: str = Field(title="", description="")
    url: str = Field(title="", description="")
    ad_id: UUID = Field(title="", description="")
    price: int = Field(title="", description="")
    make: str = Field(title="", description="")
    model: str = Field(title="", description="")
    color: str = Field(title="", description="")
    seats: int = Field(title="", description="")
    dealer_domain: str = Field(title="", description="")
    dealer_name: str = Field(title="", description="")
    seller_type: str = Field(title="", description="")
    vrm: str = Field(title="", description="")
    
    class Config:
        """Config"""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Title for ad",
                "content": "Some ad content",
                "date": "some date"
            }
        }

class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[CarResponse]
