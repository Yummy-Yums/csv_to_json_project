from contextlib import asynccontextmanager
from fastapi import FastAPI 
from app.api.healthcheck import router as health_router
from app.api.endpoints.upload_csv import router as upload_router
from app.api.endpoints.jobs import router as jobs_router
from app.models.db import create_db_and_tables
from app.utils.logger import logger

def startup():
    ## startup db
    # Ensure the database session is created at startup
    create_db_and_tables()
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is starting up...")
    startup()
    yield
    logger.info("Application is shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(upload_router)
app.include_router(jobs_router)

# for route in app.routes:
#     print(f"Route: {route.path}, Methods: {route.methods}")
    