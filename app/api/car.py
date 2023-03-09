import os
from datetime import datetime
import xml.etree.ElementTree as ET
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.core import Car, CarPicture
from app.schemas.car import CarResponse, CarSchema, CarDetailResponse, PageResponse
from app.utils import get_logger

router = APIRouter(prefix="/v1/car", tags=["Cars"])

logger = get_logger(__name__)


@router.post("/add_many", status_code=status.HTTP_201_CREATED)
async def create_multi_car(
    payload: list[CarSchema], db_session: AsyncSession = Depends(get_db)
):
    """Create multiple car"""
    try:
        file_name = "app/carplus.xml"
        file_size = 0
        if os.path.isfile(file_name):
            file_size = os.path.getsize(file_name) # Get the file size
            file_size = round(file_size / (1024 * 1024.0), 2) # Convert into MB
        file_size = '{:,.2f}'.format(file_size)
    
        tree = ET.parse(file_name)
        root = tree.getroot()
        ads = root.findall("ad")
        number_of_element = len(ads)

        for ad in ads:
            doors = 0
            print(ad.find('doors'))
            if isinstance(ad.find('doors'), ET.Element):
                doors = int(ad.find('doors').text) or 0
            seats: int = 0
            if isinstance(ad.find('seats'), ET.Element):
                seats = int(ad.find('seats').text) or 0
            year: int = 0
            if isinstance(ad.find('year'), ET.Element):
                year = int(ad.find('year').text) or 0
            mileage: int = 0
            if isinstance(ad.find('mileage'), ET.Element):
                mileage = int(ad.find('mileage').text) or 0
            engine_size: int = 0
            if isinstance(ad.find('engine_size'), ET.Element):
                engine_size = int(ad.find('engine_size').text) or 0
            priority: int = 0
            if isinstance(ad.find('priority'), ET.Element):
                priority = int(ad.find('priority').text) or 0
            color: str = ""
            if isinstance(ad.find("color"), ET.Element):
                color = ad.find("color").text or ""
            url: str = ""
            if isinstance(ad.find("url"), ET.Element):
                url = ad.find("url").text or ""
            make: str = ""
            if isinstance(ad.find("make"), ET.Element):
                make = ad.find("make").text or ""
            model: str = ""
            if isinstance(ad.find("model"), ET.Element):
                model = ad.find("model").text or ""
            post_code: str = ""
            if isinstance(ad.find("post_code"), ET.Element):
                post_code = ad.find("post_code").text or ""
            fuel: str = ""
            if isinstance(ad.find("fuel"), ET.Element):
                fuel = ad.find("fuel").text or ""
            transmission: str = ""
            if isinstance(ad.find("transmission"), ET.Element):
                transmission = ad.find("transmission").text or ""
            body_style: str = ""
            if isinstance(ad.find("bodyStyle"), ET.Element):
                body_style = ad.find("bodyStyle").text or ""
            hero_image: str = ""
            if isinstance(ad.find("hero_image"), ET.Element):
                hero_image = ad.find("hero_image").text or ""
            car_type: str = ""
            if isinstance(ad.find("car_type"), ET.Element):
                car_type = ad.find("car_type").text or ""
            dealer_domain: str = ""
            if isinstance(ad.find("dealerDomain"), ET.Element):
                dealer_domain = ad.find("dealerDomain").text or ""
            dealer_name: str = ""
            if isinstance(ad.find("dealerName"), ET.Element):
                dealer_name = ad.find("dealerName").text or ""
            seller_type: str = ""
            if isinstance(ad.find("sellerType"), ET.Element):
                seller_type = ad.find("sellerType").text or ""
            vrm: str = ""
            if isinstance(ad.find("vrm"), ET.Element):
                vrm = ad.find("vrm").text or ""
            city: str = ""
            if isinstance(ad.find("city"), ET.Element):
                city = ad.find("city").text or ""
            ad_date: datetime = None
            if isinstance(ad.find('date'), ET.Element):
                ad_date = datetime.strptime(ad.find('date').text.replace("Z","UTC"), '%Y-%m-%dT%H:%M:%S.%f%Z')

            car = Car(
                ad_id = ad.find('id').text,
                advert_id = ad.find('advertId').text,
                url = url,
                title = ad.find('title').text,
                content = ad.find('content').text or "",
                price = float(ad.find('price').text) or 0,
                make = make,
                model = model,
                color = color,
                year = year,
                post_code = post_code,
                mileage = mileage,
                doors = doors,
                fuel = fuel,
                transmission = transmission,
                body_style = body_style,
                engine_size = engine_size,
                seats = seats,
                hero_image = hero_image,
                date = ad_date,
                car_type = car_type,
                city = city,
                dealer_domain = dealer_domain,
                dealer_name = dealer_name,
                priority = priority,
                seller_type = seller_type,
                vrm = vrm
            )
            await car.save(db_session)
            car_id = car.id
            pictures = ad.find("pictures")
            if pictures:
                for picture in pictures.findall("picture"):
                    picture_url: str = ""
                    picture_url = picture.find("picture_url").text or ""
                    car_picture = CarPicture(
                        car_id = car_id,
                        url = picture_url
                    )
                    await car_picture.save(db_session)

    except SQLAlchemyError as ex:
        # logger.exception(ex)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
        ) from ex
    else:
        # logger.info(f"{len(car_instances)} instances of Car inserted into database.")
        return {
            "number_of_element": '{:,.0f}'.format(number_of_element),
            "file_size": str(file_size) + ' MB'
        }


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CarResponse)
async def create_car(
    payload: CarSchema, db_session: AsyncSession = Depends(get_db)
):
    """Create new car"""
    car = Car(title=payload.title, content=payload.content)
    await car.save(db_session)
    return car


@router.get("/{title}", response_model=CarDetailResponse)
async def find_car(
    title: str,
    db_session: AsyncSession = Depends(get_db),
):
    """Get car by title"""
    return await Car.find(db_session, title=title)


@router.get("/get/{id}", response_model=CarDetailResponse)
async def find_ad_by_id(
    id: int,
    db_session: AsyncSession = Depends(get_db),
):
    """Get car by title"""
    return await Car.find(db_session, id=id)

@router.get("/list/", response_model=PageResponse)
async def ads_list(
    limit: int = 10,
    page: int = 1,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    filter: str = Query(None, alias="filter"),
    db_session: AsyncSession = Depends(get_db)
):
    """Get cars list"""
    result = await Car.all(db_session, limit=limit, page=page, sort=sort, filter=filter)
    return result


# @router.delete("/{title}")
# async def delete_car(title: str, db_session: AsyncSession = Depends(get_db)):
    # """Delete car"""
    # car = await Car.find(db_session, title)
    # return await Car.delete(car, db_session)


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
