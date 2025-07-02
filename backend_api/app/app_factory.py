from applications.auth.router import router_auth
from applications.new_buildings.router import new_buildings_router, selected_router
from applications.users.router import router_users
from fastapi import FastAPI
from settings import settings


def get_application() -> FastAPI:
    app = FastAPI(root_path="/api", root_path_in_servers=True, debug=settings.DEBUG)
    app.include_router(router_users, prefix="/users", tags=["Users"])
    app.include_router(router_auth, prefix="/auth", tags=["Auth"])
    app.include_router(new_buildings_router, prefix="/new_buildings", tags=["NewBuildings"])
    app.include_router(selected_router, prefix="/selected", tags=["Selected"])

    return app
