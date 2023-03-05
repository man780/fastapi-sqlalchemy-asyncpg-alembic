from fastapi import FastAPI

from app.api.car import router as car_router
from app.api.system import router as system_router
from app.utils import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Cars API", version="0.4")

app.include_router(system_router)
app.include_router(car_router)


@app.on_event("startup")
async def startup_event():
    """Start up"""
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Start up"""
    logger.info("Shutting down...")
