import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from .data import database, models
from .routes import documents, projects, users
from .utils.logs import configure_logging

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI(on_startup=[configure_logging])

# https://medium.com/@sondrelg_12432/setting-up-request-id-logging-for-your-fastapi-application-4dc190aac0ea
app.add_middleware(CorrelationIdMiddleware)
# for request ID logging

app.include_router(projects.router)
app.include_router(users.router)
app.include_router(documents.router)


@app.get("/test")
async def run_test() -> str:
    return "Success"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
