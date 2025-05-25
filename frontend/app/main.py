from app_factory import get_application

app = get_application()

@app.get('/')
def for_this_project():
    return {'status': 'gradproject'}