from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import httpx

router = APIRouter()

templates = Jinja2Templates(directory='templates')


@router.get('/', name='index')
async def index(request: Request):
    context = {'request': request}
    response = templates.TemplateResponse('index.html', context=context)
    return response

@router.get('/catalog', name='catalog')
async def catalog(request: Request):
    context = {'request': request}
    response = templates.TemplateResponse('index.html', context=context)
    return response