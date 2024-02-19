import uvicorn
from fastapi import FastAPI

from .data import database, models
from .routes import projects, users

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(projects.router)
app.include_router(users.router)


@app.get("/test")
async def run_test() -> str:
    return "Success"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
