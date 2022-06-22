from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api
from app.core.db import check_db

__version__ = 0, 0, 1

api.version = '.'.join(map(str, __version__))

app = FastAPI(debug=False)
app.mount('/api', api)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

check_db(drop=True)
