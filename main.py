from fastapi import FastAPI 
from app.api.healthcheck import router as health_router
from app.api.endpoints.upload_csv import router as upload_router  

app = FastAPI()
app.include_router(health_router)
app.include_router(upload_router)


def startup():
    print("Application is starting up...")

# for route in app.routes:
#     print(f"Route: {route.path}, Methods: {route.methods}")
    