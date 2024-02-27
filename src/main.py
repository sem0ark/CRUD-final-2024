from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from src.document.endpoint import router as DocumentRouter
from src.project.endpoint import router as ProjectRouter
from src.shared.database import Base, engine
from src.shared.logs import configure_logging
from src.user.endpoint import router as UserRouter

Base.metadata.create_all(bind=engine)


app = FastAPI(on_startup=[configure_logging])

# https://medium.com/@sondrelg_12432/setting-up-request-id-logging-for-your-fastapi-application-4dc190aac0ea
app.add_middleware(CorrelationIdMiddleware)
# for request ID logging

app.include_router(ProjectRouter)
app.include_router(UserRouter)
app.include_router(DocumentRouter)


@app.get("/test")
async def run_test() -> str:
    return "Success"
