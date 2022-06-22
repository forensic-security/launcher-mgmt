from fastapi import HTTPException


class ClientError(HTTPException):
    pass


class ServerError(HTTPException):
    pass


class AuthError(ClientError):
    pass


class AuthenticationError(AuthError):
    def __init__(self, msg) -> None:
        super().__init__(
            status_code=401,
            detail=msg,
            headers={'WWW-Authenticate': 'Bearer'},
        )


class AuthorizationError(AuthError):
    def __init__(self, msg) -> None:
        super().__init__(
            status_code=403,
            detail=msg,
        )


class ContentError(ClientError):
    def __init__(self, msg) -> None:
        super().__init__(status_code=400, detail=msg)


class ResourceNotFound(ClientError):
    def __init__(self, msg) -> None:
        super().__init__(status_code=404, detail=msg)
