import os
from datetime import timedelta
from pydantic import BaseModel

DB_PASS = os.environ.get("DB_PASS")
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_ENV = os.environ.get("DB_ENV")

CONFIG_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
TEST_DATABASE_URL = "sqlite:///db.sqlite"
if DB_ENV == "TEST":
    CONFIG_DATABASE_URL = TEST_DATABASE_URL


SECRET_KEY = os.environ.get('SECRET_KEY')
if SECRET_KEY is None:
    SECRET_KEY = '123123123123'

jwt_alg = "HS512"
access_token_exp = timedelta(days=30)
refresh_token_exp = timedelta(days=60)

# CORS
ORIGINS = ['*']


# COOKIES
class BaseJWTCookie(BaseModel):
    """ Базовая настройка куки """
    path: str = '/'
    httponly: bool = True
    samesite: str = "lax"
    value: str = 'null'


class RefreshCookie(BaseJWTCookie):
    """ Куки Refresh токена """
    key: str = 'refresh_token'
    path: str = '/refresh'


class AccessCookie(BaseJWTCookie):
    """ Куки Access токена """
    key: str = 'access_token'