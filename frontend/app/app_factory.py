from fastapi import FastAPI

from settings import settings


def get_application() -> FastAPI:
    app = FastAPI(root_path_in_servers=True, debug=settings.DEBUG)
    return app