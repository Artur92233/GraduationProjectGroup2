from fastapi import FastAPI


app = FastAPI(root_path="/api", root_path_in_servers=True)


@app.get("/")
async def index():
    return {"status2332": 200}
