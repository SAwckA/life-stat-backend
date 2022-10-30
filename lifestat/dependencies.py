from fastapi import Cookie
from lifestat.jwt_tokens import JWTAccessToken


def validate(token):
    user = JWTAccessToken.validate_token(token)
    if isinstance(user, JWTAccessToken.AccessPayload):
        return user
    raise user


class PasswordAuth: ...


class Register: ...


class AccessTokenAuth:
    def __init__(
                self,
                access_token: str = Cookie('access_token')
                ):
        self.user: JWTAccessToken.AccessPayload = validate(access_token)
