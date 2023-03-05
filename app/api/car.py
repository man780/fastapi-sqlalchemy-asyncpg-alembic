from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.core import Car
from app.schemas.car import CarResponse, CarSchema
from app.utils import get_logger

router = APIRouter(prefix="/v1/car", tags=["Cars"])

logger = get_logger(__name__)


@router.post("/add_many", status_code=status.HTTP_201_CREATED)
async def create_multi_car(
    payload: list[CarSchema], db_session: AsyncSession = Depends(get_db)
):
    """Create multiple car"""
    try:
        car_instances = [
            Car(title=car.title, description=car.description) for car in payload
        ]
        db_session.add_all(car_instances)
        await db_session.commit()
    except SQLAlchemyError as ex:
        # logger.exception(ex)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
        ) from ex
    else:
        logger.info(f"{len(car_instances)} instances of Car inserted into database.")
        return True


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CarResponse)
async def create_car(
    payload: CarSchema, db_session: AsyncSession = Depends(get_db)
):
    """Create new car"""
    car = Car(title=payload.title, content=payload.content)
    await car.save(db_session)
    return car


@router.get("/{title}", response_model=CarResponse)
async def find_car(
    title: str,
    db_session: AsyncSession = Depends(get_db),
):
    """Get car by title"""
    return await Car.find(db_session, title)

@router.get("/all/{title}", response_model=list)
async def all(
    db_session: AsyncSession = Depends(get_db),
):
    """Get cars list"""
    return await Car.all(db_session)


@router.delete("/{title}")
async def delete_car(title: str, db_session: AsyncSession = Depends(get_db)):
    """Delete car"""
    car = await Car.find(db_session, title)
    return await Car.delete(car, db_session)


@router.patch("/{title}", response_model=CarResponse)
async def update_car(
    payload: CarSchema,
    title: str,
    db_session: AsyncSession = Depends(get_db),
):
    """Update car"""
    car = await Car.find(db_session, title)
    await car.update(db_session, **payload.dict())
    return car
