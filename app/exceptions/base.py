class AppException(Exception):
    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)

class NotFoundException(AppException):
    status_code = 404
    detail = "Resource not found"

class BadRequestException(AppException):
    status_code = 400
    detail = "Bad request"