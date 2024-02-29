from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

import src.document.endpoint as document_routes
import src.logo.endpoint as logo_routes
import src.project.endpoint as project_routes
import src.user.endpoint as user_routes
from src.shared.database import Base, engine
from src.shared.logs import configure_logging

Base.metadata.create_all(bind=engine)


app = FastAPI(on_startup=[configure_logging])

# https://medium.com/@sondrelg_12432/setting-up-request-id-logging-for-your-fastapi-application-4dc190aac0ea
app.add_middleware(CorrelationIdMiddleware)
# for request ID logging

app.include_router(document_routes.router)
app.include_router(project_routes.router)
app.include_router(user_routes.router)
app.include_router(logo_routes.router)


@app.get("/test")
async def run_test() -> str:
    return "Success"
