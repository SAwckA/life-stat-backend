""" Алгоритмы работы jwt в auth сервисе"""

import base64
import os
import datetime
import jwt as json_web_token
import lifestat.utils.hash_algs as hash_algs
from abc import ABC
from fastapi import HTTPException
from pydantic import BaseModel

from lifestat.schemes import Message

import settings.config


SECRET_KEY = "mkjhgfcfvghbjn,k.bjvhcgxfdfgkl;oiuiytuyrerswertyuytrty6543456787654q23rtyjku5432we"


class TokensPair(BaseModel):
    """ Объект представления пары токенов (замена обращений со словарей на типипзированные классы) """
    access: str
    refresh: str


class BaseTokenPayload(BaseModel):
    """ Базовая полезная нагрузка токена """
    jti: str = None
    sub: str
    iss: str


class AbstractJWT(ABC):
    """ Интерфейс токена """
    payload_class: BaseTokenPayload = BaseTokenPayload
    token_type: str

    @classmethod
    def encode_token(cls, data: payload_class, sid: str = None) -> tuple[str, str]:
        """ Возвращает токен и sid """
        ...

    @classmethod
    def decode_token(cls, token: str) -> payload_class:
        """ Возвращает полезную нагрузку токена """
        ...

    @classmethod
    def validate_token(cls, token: str) -> payload_class:
        """ Проверяет полученный токен """
        ...

    @classmethod
    def check_sub(cls, token_payload: payload_class) -> payload_class:
        """ Проверяет назначение токена """


class BaseJWT(AbstractJWT):
    """ Базовая реализация jwt токена"""

    payload_class: BaseTokenPayload = BaseTokenPayload
    token_type: str

    @classmethod
    def get_exp_time(cls, token_type: str) -> int:
        """ Установка времени истечения токена """

        match token_type:
            case "access":
                time_delta = settings.config.access_token_exp

            case "refresh":
                time_delta = settings.config.refresh_token_exp

            case _:
                time_delta = settings.config.access_token_exp

        return int(datetime.datetime.now().timestamp()) + int(time_delta.total_seconds())

    @classmethod
    def create_sid(cls):
        """
            Уникальная строка сессии
            Создаётся 1 раз, при логине по паролю
            Наследуется новыми refresh токенами
        """
        return hash_algs.generate_token_sid()

    @classmethod
    def create_jti(cls):
        """ Уникальная строка токена, используется как id """
        return base64.b64encode(os.urandom(18)).decode('utf-8')

    @classmethod
    def encode_token(cls, data: payload_class, sid: str = None, token_type: str = None) -> tuple[str, str]:
        """ Шифровка токена """
        payload = cls.payload_class(**(data.dict())).dict()
        payload['jti'] = base64.b64encode(os.urandom(18)).decode('utf-8')
        payload['exp'] = cls.get_exp_time(cls.token_type)

        if sid is None:
            sid = cls.create_sid()

        payload['sid'] = sid

        token = json_web_token.encode(payload=payload, key=SECRET_KEY, algorithm=settings.config.jwt_alg)
        return token, sid

    @classmethod
    def decode_token(cls, token: str) -> payload_class:
        """ Расшифровка токена """
        header = json_web_token.get_unverified_header(token)

        payload: dict = json_web_token.decode(
            token,
            key=SECRET_KEY,
            algorithms=[header.get('alg'), ]
        )

        return cls.payload_class(**payload)

    @classmethod
    def validate_token(cls, token: str) -> payload_class | HTTPException:
        """ Валидация токена для расшифровки """
        try:
            payload = cls.decode_token(token)

        except (json_web_token.ExpiredSignatureError, json_web_token.DecodeError) as e:

            if isinstance(e, json_web_token.ExpiredSignatureError):
                return HTTPException(status_code=401,
                                     detail=Message(status_code=702,
                                                    message="Token is expired").dict())

            if isinstance(e, json_web_token.DecodeError):
                return HTTPException(status_code=401,
                                     detail=Message(status_code=703,
                                                    message="Invalid token").dict())

            return HTTPException(status_code=401,
                                 detail=Message(status_code=760,
                                                message=f"Access token error: {e}").dict())

        return payload

    @classmethod
    def check_sub(cls, token_payload: payload_class) -> payload_class | HTTPException:
        """ Проверка назначения """
        if token_payload.sub == cls.token_type:
            return token_payload
        return HTTPException(status_code=401,
                             detail=Message(status_code=701,
                                            message="Invalid token sub").dict())


class JWTRefreshToken(BaseJWT):
    """ Реализация refresh токена """

    class RefreshPayload(BaseTokenPayload):
        """ Полезная нагрузка refresh токена """
        id: int
        username: str = None
        is_verified: bool = False
        sid: str = None
        # RFC Standard
        iss: str = 'auth_service'
        sub: str = 'refresh'

    payload_class = RefreshPayload
    token_type = 'refresh'

    @classmethod
    def encode_token(cls, data: payload_class, sid: str = None, token_type: str = token_type) -> tuple[str, str]:
        """ Переопределение класса полезной нагрузки"""
        return super().encode_token(data, sid, token_type)


class JWTAccessToken(BaseJWT):
    """ Реализация access токена """

    class AccessPayload(BaseTokenPayload):
        """ Полезная нагрузка access токена """

        # App service info
        id: int
        username: str
        
        # Custom services
        sid: str = None

        # RFC Standard
        sub: str = "access"
        iss: str = "auth_service"

    payload_class = AccessPayload
    token_type = 'access'

    @classmethod
    def encode_token(cls, data: payload_class, sid: str = None, token_type: str = token_type) -> tuple[str, str]:
        """ Переопределение класса полезной нагрузки"""
        return super().encode_token(data, sid, token_type)
