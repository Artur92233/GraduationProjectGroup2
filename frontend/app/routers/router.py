from backend_api_in_frontend.api import (get_building, get_current_user_with_token, get_new_buildings, get_rents,
                                         get_second_owners, login_user, register_user, sell_buildings)
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from new_buildings_schema import SortTypeByEnum

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", name="index")
@router.post("/")
async def index(request: Request, query: str = Form(""), user: dict = Depends(get_current_user_with_token)):
    new_building = await get_building(query)
    context = {
        "request": request,
        "new_building": new_building,
    }
    if user.get("name"):
        context["user"] = user
    response = templates.TemplateResponse("index.html", context=context)
    return response


@router.get("/new_buildings", name="new_buildings")
async def new_buildings(
    request: Request, user: dict = Depends(get_current_user_with_token), new_buildings=Depends(get_new_buildings)
):
    context = {
        "request": request,
        "user": user,
        "new_buildings": new_buildings["items"],  # Обрабатываем результат зависимости здесь
    }
    return templates.TemplateResponse("new_buildings.html", context=context)


@router.get("/new_buildings/{new_building_id}")
async def new_building_detail(
    request: Request, new_building_id: int, user: dict = Depends(get_current_user_with_token)
):
    new_building = await get_building(new_building_id)
    context = {
        "request": request,
        "new_building": new_building,
    }
    if user.get("name"):
        context["user"] = user
    response = templates.TemplateResponse("new_building_detail.html", context=context)
    return response


@router.get("/rent", name="rent")
async def for_rent(request: Request, user: dict = Depends(get_current_user_with_token), rent=Depends(get_rents)):
    context = {"request": request, "user": user, "rents": rent["items"]}  # Обрабатываем результат зависимости здесь
    return templates.TemplateResponse("rent.html", context=context)


@router.get("/rent/{rent_id}", name="rent_detail")
async def rent_detail(
    request: Request,
    rent_id: int,
    user: dict = Depends(get_current_user_with_token),
):
    rent = await get_building(rent_id)
    context = {
        "request": request,
        "rent": rent,
    }
    if user.get("name"):
        context["user"] = user
    return templates.TemplateResponse("rent_detail.html", context=context)


@router.get("/second_owner", name="second_owner")
async def second_owner(
    request: Request, user: dict = Depends(get_current_user_with_token), second_owner=Depends(get_second_owners)
):
    context = {
        "request": request,
        "user": user,
        "second_owners": second_owner["items"],
    }
    return templates.TemplateResponse("second_owner.html", context=context)


@router.post("/sell_buildings", name="sell_buildings")
async def post_sell_buildings(
    request: Request,
    user: dict = Depends(get_current_user_with_token),
    rent=Depends(get_rents),
    second_owner=Depends(get_second_owners),
):
    building = sell_buildings()
    context = {"request": request, "user": user, "building": building, "rent": rent, "second_owner": second_owner}

    return templates.TemplateResponse("sell_buildings.html", context=context)


@router.get("/sell_buildings")
async def sell_building_form(request: Request, user: dict = Depends(get_current_user_with_token)):
    building_sell_form = sell_buildings()
    return templates.TemplateResponse(
        "sell_buildings.html", {"request": request, "user": user, "building": building_sell_form}
    )


@router.get("/second_owner/{second_owner_id}", name="second_owner_detail")
async def second_owner_detail(
    request: Request,
    second_owner_id: int,
    user: dict = Depends(get_current_user_with_token),
):
    second_owner = await get_building(second_owner_id)
    context = {
        "request": request,
        "second_owner": second_owner,
    }
    if user.get("name"):
        context["user"] = user
    return templates.TemplateResponse("second_owner_detail.html", context=context)


async def get_sell_buildings_data():
    # Здесь логика получения данных, например через API/БД
    # Пример: .
    # return await some_api_call()
    return [...]  # возвращай данные для шаблона


@router.post("/sell_building", name="sell_building")
async def sell_building(
    request: Request,
    user: dict = Depends(get_current_user_with_token),
    rents=Depends(get_rents),
    new_building=Depends(get_new_buildings),
):
    building = await sell_buildings()
    sort = SortTypeByEnum
    for building in building:
        if building.type == sort.NEW_BUILDING:
            building.append(new_building)
        elif building.type == sort.FOR_RENT:
            building.append(rents)
        elif building.type == sort.SECOND_OWNER:
            building.append(rents)
    context = {"request": request, "user": user, "sell_buildings": building}

    return templates.TemplateResponse("sell_building.html", context=context)


@router.get("/profile", name="personal_account")
async def profile(request: Request, user: dict = Depends(get_current_user_with_token)):
    if not user:
        return templates.TemplateResponse(
            "login.html", {"request": request, "user": {}, "errors": ["Увійдіть, щоб переглянути кабінет"]}
        )
    return templates.TemplateResponse("personal_account.html", {"request": request, "user": user})


@router.get("/blog", name="blog")
async def blog(request: Request, user: dict = Depends(get_current_user_with_token)):
    context = {"request": request, "user": user}
    return templates.TemplateResponse("blog.html", context=context)


@router.get("/login")
@router.post("/login")
async def login(
    request: Request,
    user: dict = Depends(get_current_user_with_token),
    user_email: str = Form(""),
    password: str = Form(""),
):
    context = {"request": request, "entered_email": user_email}
    redirect_url = request.url_for("index")
    if user.get("name"):
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        return response

    if request.method == "GET":
        response = templates.TemplateResponse("login.html", context=context)
        response.delete_cookie("access_token")
        return response

    user_tokens = await login_user(user_email, password)
    access_token = user_tokens.get("access_token")
    if not access_token:
        errors = ["Неправильна електронна пошта або пароль"]
        context["errors"] = errors
        return templates.TemplateResponse("login.html", context=context)
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=60 * 5)
    return response


@router.get("/logout")
async def logout(request: Request):
    redirect_url = request.url_for("login")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response


@router.get("/register")
@router.post("/register")
async def register(
    request: Request,
    user: dict = Depends(get_current_user_with_token),
    user_email: str = Form(""),
    password: str = Form(""),
    user_name: str = Form(""),
):
    context = {"request": request, "entered_email": user_email, "entered_name": user_name}
    redirect_url = request.url_for("index")
    if user.get("name"):
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        return response

    if request.method == "GET":
        response = templates.TemplateResponse("register.html", context=context)
        response.delete_cookie("access_token")
        return response

    created_user = await register_user(user_email=user_email, password=password, name=user_name)
    if created_user.get("email"):
        user_tokens = await login_user(user_email, password)
        access_token = user_tokens.get("access_token")
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=60 * 5)
        return response

    context["errors"] = [created_user["detail"]]
    response = templates.TemplateResponse("register.html", context=context)
    return response
