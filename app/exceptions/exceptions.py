class BaseApiException(Exception):
    """Base exception class"""

    def __init__(self, detail: str):
        self.detail = detail


class ServiceException(BaseApiException):
    """Failures in the service layer"""

    pass


class ValidationException(BaseApiException):
    """Validation errors"""

    pass


class FileUploadException(BaseApiException):
    """File upload errors"""

    pass
