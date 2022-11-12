import logging
import os

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.requests import Request

from elasticapm.contrib.starlette import ElasticAPM, make_apm_client

def setup_tracing() -> None:
    if not os.getenv('ELASTIC_APM_SERVICE_NAME'):
        return

    apm = make_apm_client()
    app.add_middleware(ElasticAPM, client=apm)


from lifestat.database import database_class


app = FastAPI()
db = database_class()


@app.middleware('http')
async def options_plug(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = 'http://0.0.0.0:5173'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        response.status_code = 204
        return response
    
    response = await call_next(request)
    
    response.headers['Access-Control-Allow-Origin'] = 'http://0.0.0.0:5173'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    
    return response

setup_tracing()
import lifestat.routes  # noqa # for