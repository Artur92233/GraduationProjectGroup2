from fastapi import FastAPI

from settings import settings
from routers.router import router

def get_application() -> FastAPI:
    app = FastAPI(root_path_in_servers=True, debug=settings.DEBUG)
    app.include_router(router)
    return app