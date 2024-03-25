import sys
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from app.config import settings
from app.api.api_v1.api import api_router
from app.errors.app_errors import BaseError


app = FastAPI()


try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ModuleNotFoundError:
    pass

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Assistant",
        version="1.0.0",
        description="The gpt-3.5-turbo-based assistant allows users to upload pdf "
        "documents and ask questions related to those documents.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(api_router)


@app.exception_handler(BaseError)
async def custom_exception_handler(_: Request, exc: BaseError):
    return JSONResponse(status_code=exc.code, content={"detail": exc.detail})
