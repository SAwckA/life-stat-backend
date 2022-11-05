import json

from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import Response

from lifestat.app import app, db
from lifestat.dependencies import AccessTokenAuth
from lifestat.jwt_tokens import JWTAccessToken
from lifestat.schemes import Message, RegisterForm, LoginForm, HTTPError, Data


@app.get('/')
async def index(request: Request) -> HTMLResponse:
    return "`213"


@app.get('/health')
async def health_check(request: Request):
    return 'OK'


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
    
    if len(credentials.username) <= 4:
        return Message(message='username must be > 4', status_code=101)

    try:
        db.exec_commit(sql, [credentials.username, credentials.password])

    except db.unique_exception:
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
    
    # db.cur.execute(sql, (credentials.username,))
    # user = db.cur.fetchone()
    
    user = db.fetchone(sql, [credentials.username])
    print(user)
    if user:
        if user[0] == credentials.password:

            token, _ = JWTAccessToken.encode_token(JWTAccessToken.AccessPayload(username=user[1], id=user[2]))                    
    
            response.status_code = 200
            response.set_cookie(key = "access_token", value = token, httponly=True)

            return response

    raise HTTPException(status_code=403, detail="invalid credentials")


@app.get('/protected',
    responses={
        200: {"model": Message},
        403: {"model": HTTPError, "description": "unauthorized"}
    }
)
async def protected_method(credentials: AccessTokenAuth = Depends(AccessTokenAuth)) -> Message:

    return Message(message=credentials.user.username)
    

@app.get('/allCounters')
async def get_all_counters(credentials: AccessTokenAuth = Depends(AccessTokenAuth)):
    sql = "SELECT all_counters FROM public.user WHERE id=%s"

    # db.cur.execute(sql, (credentials.user.id, ))
    # counters = db.cur.fetchone()

    counters = db.fetchone(sql, [credentials.user.id])
    print(counters)
    if counters:
        if counters[0] != [] or counters[0] != "[]":
            if isinstance(counters[0], str):
                counters = json.loads(counters[0])
                return counters
            return counters[0]
    return [None,]


@app.post('/saveCounters')
async def save_all_counters(counters: list, credentials: AccessTokenAuth = Depends(AccessTokenAuth)) -> Message:
    sql = """UPDATE public.user SET all_counters=%s WHERE id=%s"""

    # db.cur.execute(sql, (json.dumps(counters), credentials.user.id))
    # db.conn.commit()

    db.exec_commit(sql, [json.dumps(counters), credentials.user.id])

    return Message(message="success")


@app.get('/theme')
async def get_theme(credentials: AccessTokenAuth = Depends(AccessTokenAuth)) -> dict:
    sql = """SELECT theme FROM public.user WHERE id=%s"""
    
    # db.cur.execute(sql, (credentials.user.id, ))
    # theme = db.cur.fetchone()
    theme = db.fetchone(sql, [credentials.user.id])
    print(theme)
    if theme:
        if theme[0] != [] or theme[0] != "[]":
            if isinstance(theme[0], str):
                theme = json.loads(theme[0])
                return theme
            return theme[0]
    return [None,]


@app.post('/saveTheme')
async def save_theme(theme: dict, credentials: AccessTokenAuth = Depends(AccessTokenAuth)) -> Message:
    sql = """UPDATE public.user SET theme=%s WHERE id=%s"""

    # db.cur.execute(sql, (json.dumps(theme), credentials.user.id))
    # db.conn.commit()

    db.exec_commit(sql, [json.dumps(theme), credentials.user.id])

    return Message(message="success", status_code=0)


@app.get('/user')
async def get_user(credentials: AccessTokenAuth = Depends(AccessTokenAuth)) -> Message:
    
    return Message(status_code=0, message=credentials.user.username)

    