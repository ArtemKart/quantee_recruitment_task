import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from app.api.routers.upload import upload_router
from app.exceptions.exception_handler import create_exception_handler
from app.exceptions.exceptions import (
    FileUploadException,
    ServiceException,
    ValidationException,
)

app = FastAPI()

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


app.include_router(upload_router)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
