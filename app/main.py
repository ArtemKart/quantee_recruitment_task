import logging
import os
from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from app.api import get_api_prefix, get_api_version
from app.api.routers.upload import main_router
from app.exceptions.exception_handler import create_exception_handler
from app.exceptions.exceptions import (
    DatabaseException,
    FileUploadException,
    ServiceException,
    ValidationException,
)

logging.basicConfig(level=logging.INFO)


if os.getenv(key="USE_PROXY", default="").lower() == "true":
    settings = dict(
        title="quantee-api",
        version=get_api_version(),
        servers=[{"url": get_api_prefix()}],
        root_path=get_api_prefix(),
    )
else:
    settings = dict(
        title="quantee-api",
        version=get_api_version(),
    )

app: Final = FastAPI(**settings)

request_origins = [
    "http://localhost",
    "http://127.0.0.1",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=request_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(main_router)

app.add_exception_handler(
    exc_class_or_status_code=ServiceException,
    handler=create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Service Exception"
    ),
)
app.add_exception_handler(
    exc_class_or_status_code=ValidationException,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Validation Exception"
    ),
)
app.add_exception_handler(
    exc_class_or_status_code=FileUploadException,
    handler=create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Exception occurred while uploading file",
    ),
)
app.add_exception_handler(
    exc_class_or_status_code=DatabaseException,
    handler=create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Exception occurred during interaction with database",
    ),
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
