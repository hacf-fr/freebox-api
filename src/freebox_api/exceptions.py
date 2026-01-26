class InvalidTokenError(Exception):
    pass


class NotOpenError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class HttpRequestError(Exception):
    pass


class InsufficientPermissionsError(HttpRequestError):
    pass
