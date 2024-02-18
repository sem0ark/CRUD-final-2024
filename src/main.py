import uvicorn
from fastapi import FastAPI

from src.data import database, models
from src.routes import projects

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(projects.router)


@app.get("/test")
async def run_test() -> str:
    return "Success"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
