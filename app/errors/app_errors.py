from starlette import status


class BaseError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.code = status_code
        self.detail = detail


class UnsupportedFileExtensionError(BaseError):
    def __init__(self):
        status_code = status.HTTP_400_BAD_REQUEST
        detail = "The document must be in pdf format"
        super(UnsupportedFileExtensionError, self).__init__(
            status_code=status_code, detail=detail
        )
