class FreeboxException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InvalidTokenError(FreeboxException):
    """Invalid Token Error."""


class NotOpenError(FreeboxException):
    """Not Open Error."""


class AuthorizationError(FreeboxException):
    """Authorization Error."""


class HttpRequestError(FreeboxException):
    """HTTP Request Error."""


class InsufficientPermissionsError(HttpRequestError):
    """Insufficient Permissions Error."""
