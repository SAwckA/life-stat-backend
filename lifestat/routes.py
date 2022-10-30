import logging
import json

from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import Response
from starlette.templating import _TemplateResponse
from pydantic import BaseModel

from psycopg2.errors import UniqueViolation

from lifestat.app import app, db
from lifestat.dependencies import AccessTokenAuth
from lifestat.jwt_tokens import JWTAccessToken
from lifestat.schemes import Message, RegisterForm, LoginForm, HTTPError


@app.get('/')
async def index(request: Request) -> HTMLResponse:
    return "`213"


@app.post('/register', responses={
    200: {
            "model": Message
        },
    409: {
            "model": HTTPError,
            "description": "database error"
    }    
})
async def register(credentials: RegisterForm) -> Message:
    sql = """insert into public.user(username, password) values
            (%s, %s);"""
    try:
        db.cur.execute(sql, (credentials.username, credentials.password, ))
        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise HTTPException(status_code=409, detail="username already exist")

    return Message(message='ok')


@app.post('/login',
    responses={
        200: {"model": Message},
        403: {"model": HTTPError, "description": ")"}
    })
async def login(response: Response, credentials: LoginForm) -> Message:
    sql = """SELECT password, username, id FROM public.user WHERE username=%s"""
    db.cur.execute(sql, (credentials.username,))
    user = db.cur.fetchone()
    if user:
        if user[0] == credentials.password:

            token, _ = JWTAccessToken.encode_token(JWTAccessToken.AccessPayload(username=user[1], id=user[2]))                    
            print(token)
            response.status_code = 200
            response.set_cookie(key = "access_token", value = token)

            return response

    raise HTTPException(status_code=403, detail="invalid credentials")


@app.get('/protected',
    responses={
        200: {"model": Message},
        403: {"model": HTTPError, "description": "unauthorized"}
    }
)
async def protected_method(credentials: AccessTokenAuth = Depends(AccessTokenAuth)) -> Message:
    print(credentials.user)
    
    return Message(message=credentials.user.username)
    

@app.get('/allCounters')
async def get_all_counters(credentials: AccessTokenAuth = Depends(AccessTokenAuth)):
    sql = "SELECT all_counters FROM public.user WHERE id=%s"
    db.cur.execute(sql, (credentials.user.id, ))
    counters = db.cur.fetchone()
    print(counters)
    return counters[0]


@app.post('/saveCounters')
async def save_all_counters(counters: list, credentials: AccessTokenAuth = Depends(AccessTokenAuth)) -> Message:
    sql = """UPDATE public.user SET all_counters=%s WHERE id=%s"""

    db.cur.execute(sql, (json.dumps(counters), credentials.user.id))
    db.conn.commit()

    return Message(message="success")
