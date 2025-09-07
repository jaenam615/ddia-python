from fastapi import APIRouter

from chatper_10.api.service import UserService

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()

@router.get("/")
async def list_users():
    return service.get_users()