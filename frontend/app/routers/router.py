from backend_api_in_frontend.api import (
    get_building,
    get_current_user_with_token,
    get_new_buildings,
    get_rents,
    get_second_owners,
    login_user,
    register_user,
    sell_buildings,
)
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
    response = templates.TemplateResponse(request, context=context, name="index.html")
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
    return templates.TemplateResponse(request, context=context, name="new_buildings.html")


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
    response = templates.TemplateResponse(request, context=context, name="new_building_detail.html")
    return response


@router.get("/rent", name="rent")
async def for_rent(request: Request, user: dict = Depends(get_current_user_with_token), rent=Depends(get_rents)):
    context = {"request": request, "user": user, "rents": rent["items"]}  # Обрабатываем результат зависимости здесь
    return templates.TemplateResponse(
        request,
        context=context,
        name="rent.html",
    )


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
    return templates.TemplateResponse(
        request,
        context=context,
        name="rent_detail.html",
    )


@router.get("/second_owner", name="second_owner")
async def second_owner(
    request: Request, user: dict = Depends(get_current_user_with_token), second_owner=Depends(get_second_owners)
):
    context = {
        "request": request,
        "user": user,
        "second_owners": second_owner["items"],
    }
    return templates.TemplateResponse(request, context=context, name="second_owner.html")


@router.post("/sell_buildings", name="sell_buildings")
async def post_sell_buildings(
    request: Request,
    user: dict = Depends(get_current_user_with_token),
    rent=Depends(get_rents),
    second_owner=Depends(get_second_owners),
):
    building = sell_buildings()
    context = {"request": request, "user": user, "building": building, "rent": rent, "second_owner": second_owner}

    return templates.TemplateResponse(request, context=context, name="sell_buildings.html")


@router.get("/sell_buildings")
async def sell_building_form(request: Request, user: dict = Depends(get_current_user_with_token)):
    building_sell_form = sell_buildings()
    return templates.TemplateResponse(
        request=request,
        name="sell_buildings.html",
        context={"user": user, "building": building_sell_form}
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
    return templates.TemplateResponse(request, context=context, name="second_owner_detail.html")


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
    # 1. Получаем список зданий (переименовали во множественное число)
    buildings_list = await sell_buildings()
    sort = SortTypeByEnum

    # 2. Перебираем список, используя правильные имена переменных
    for item in buildings_list:
        if item.type == sort.NEW_BUILDING:
            # Используем установку атрибута, а не .append()
            item.attached_data = new_building
        elif item.type == sort.FOR_RENT:
            item.attached_data = rents
        elif item.type == sort.SECOND_OWNER:
            item.attached_data = rents

    # 3. Передаем в контекст весь измененный список
    context = {
        "request": request,
        "user": user,
        "sell_buildings": buildings_list  # Теперь здесь валидный список
    }

    return templates.TemplateResponse(request, context=context, name="second_owner_detail.html")


@router.get("/profile", name="personal_account")
async def profile(request: Request, user: dict = Depends(get_current_user_with_token)):
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"user": {}, "errors": ["Увійдіть, щоб переглянути кабінет"]}
        )
    return templates.TemplateResponse(request=request, name="personal_account.html", context={"user": user})


@router.get("/blog", name="blog")
async def blog(request: Request, user: dict = Depends(get_current_user_with_token)):
    context = {"request": request, "user": user}
    return templates.TemplateResponse(context=context, name="blog.html")


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
        response = templates.TemplateResponse(request, context=context, name="login.html")
        response.delete_cookie("access_token")
        return response

    user_tokens = await login_user(user_email, password)
    access_token = user_tokens.get("access_token")
    if not access_token:
        errors = ["Неправильна електронна пошта або пароль"]
        context["errors"] = errors
        return templates.TemplateResponse(request, context=context, name="login.html")
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
        response = templates.TemplateResponse(
            request,
            context=context,
            name="register.html",
        )
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
    response = templates.TemplateResponse(context=context, name="register.html")
    return response
