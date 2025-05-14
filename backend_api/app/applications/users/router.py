from fastapi import APIRouter

router_users = APIRouter()


@router_users.get("/")
async def index():
    return []
