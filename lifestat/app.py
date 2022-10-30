import logging
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from lifestat.database import Database

app = FastAPI()
db = Database(user="testuser", password="qwerty", db="testdb", host="db")



# def setup_logging() -> None:
#     file_handler = logging.FileHandler(os.getenv('LOG_PATH', 'russky.log'))
#     file_handler.setFormatter(ecs_logging.StdlibFormatter())
#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(
#         logging.Formatter(
#             os.getenv(
#                 'LOF_FORMAT',
#                 '%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
#             )
#         )
#     )
#     logging.basicConfig(
#         level=logging.INFO,
#         handlers=[file_handler, console_handler],
#     )


import lifestat.routes  # noqa # for