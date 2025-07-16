from fastapi import APIRouter

router = APIRouter(prefix="/health_check", tags=["Health Check Endpoint"])

@router.get("")
def health_check():
    return {"Hello": "World"}

# check if the health check function is called, if the databse is connected, etc