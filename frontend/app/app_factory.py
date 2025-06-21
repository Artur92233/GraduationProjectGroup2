from fastapi import FastAPI
from routers.router import router
from settings import settings
from fastapi.staticfiles import StaticFiles


def get_application() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG)
    app.include_router(router)
    app.mount('/static', StaticFiles(directory='static'), name='static')
    return app
