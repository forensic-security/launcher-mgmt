from fastapi import FastAPI

from ._router import crud_router
from .crm import customer
from .user import auth, user
from ..core.db import add_pagination
from ..models.crm import Device, UpdateDevice

device = crud_router(Device, False, UpdateDevice, delete=False)

api = FastAPI(
    title='Launcher Management',
    contact={
        'url': 'https://forensic-security.com/contactar/',
        'email': 'info@forensic-security.com',
    },
)

api.include_router(auth)
api.include_router(user)
api.include_router(customer)
api.include_router(device)

add_pagination(api)
