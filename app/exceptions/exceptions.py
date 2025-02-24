class BaseApiException(Exception):
    """Base exception class"""

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)


class ServiceException(BaseApiException):
    """General failures"""

    pass


class ValidationException(BaseApiException):
    """Validation errors"""

    pass


class FileUploadException(BaseApiException):
    """File upload errors"""

    pass


class DatabaseException(BaseApiException):
    """Database errors"""

    pass


class RequestException(BaseApiException):
    """Request errors"""

    pass
