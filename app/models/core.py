import math
from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import (
    Column, String, select, Integer, Boolean, DateTime, Float, ForeignKey, PrimaryKeyConstraint, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Mapped

from app.models.base import Base
from app.schemas.car import PageResponse


class Car(Base):
    """Car model"""
    __tablename__ = "car"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="car_pkey"),
        {"schema": "core"}
    )
    id = Column(Integer, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    ad_id = Column(UUID(as_uuid=True))
    advert_id = Column(UUID(as_uuid=True))
    url = Column(String, nullable=False)
    price = Column(Float, nullable=False, default=0)
    make = Column(String, nullable=False, default="")
    model = Column(String, nullable=False, default="")
    color = Column(String, nullable=False, default="")
    year = Column(Integer, nullable=False, default=0)
    city = Column(String, nullable=False, default="")
    post_code = Column(String, nullable=False, default="")
    mileage = Column(Integer, nullable=False, default=0)
    doors = Column(Integer, nullable=False, default=0)
    fuel = Column(String, nullable=False, default="")
    transmission = Column(String, nullable=False, default="")
    body_style = Column(String, nullable=False, default="")
    engine_size = Column(Integer, nullable=False, default=0)
    seats = Column(Integer, nullable=False, default=0)
    hero_image = Column(String, nullable=False, default="")
    date = Column(DateTime, default=datetime.now())
    car_type = Column(String, nullable=False, default="")
    dealer_domain = Column(String, nullable=False, default="")
    dealer_name = Column(String, nullable=False, default="")
    priority = Column(Integer, nullable=False, default=0)
    seller_type = Column(String, nullable=False, default="")
    vrm = Column(String, nullable=False, default="")

    active = Column(Boolean, nullable=True, default=True)
    created = Column(DateTime, default=datetime.now())

    car_pictures: Mapped[List["CarPicture"]] = relationship("CarPicture", back_populates="car", lazy='selectin')

    @classmethod
    async def find(cls, db_session: AsyncSession, title: str = None, id: int = None):
        """

        :param db_session:
        :param title:
        :return:
        """
        if title:
            stmt = select(cls).where(cls.title == title)
        else:
            stmt = select(cls).where(cls.id == id)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        print(instance)
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Not found": f"There is no record for name: {title}"},
            )
        else:
            return instance

    @classmethod
    async def all(
        cls, db_session: AsyncSession,
        limit: int = 10,
        page: int = 1,
        columns: str = None,
        sort: str = None,
        filter: str = None
    ):
        """
        
        :param db_session:
        :return:
        """
        offset_page: int = (page - 1 )
        offset: int = offset_page * limit
        stmt = select(cls).where(cls.active == True)
        stmt = stmt.offset(offset).limit(limit).order_by(cls.date.desc())
        result = await db_session.execute(stmt)
        instance = result.scalars().all()

        # count query
        count_query = select(func.count(1)).select_from(select(cls).where(cls.active == True))
        # total record
        total_record = (await db_session.execute(count_query)).scalar() or 0
        # total page
        total_page = math.ceil(total_record / limit)

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Not found": "Data not found"},
            )
        else:
            return PageResponse(
                content=instance,
                page_number=page,
                page_size=limit,
                total_pages=total_page,
                total_record=total_record,
            )


class CarPicture(Base):
    """Cars pictures"""
    __tablename__ = "car_picture"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="car_picture_pkey"),
        {"schema": "core"},
    )
    id: Mapped[int] = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    car_id: Mapped[int] = Column(ForeignKey("core.car.id"), nullable=False)
    url: str = Column(String, nullable=False)
    active: bool = Column(Boolean, nullable=True, default=True)

    car: Mapped["Car"] = relationship("Car", back_populates="car_pictures")
