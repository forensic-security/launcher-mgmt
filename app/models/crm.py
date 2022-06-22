from ..core.model import Schema, DatedMixin, Field, Relationship
from ._types import EmailStr, UUID, StrEnum


class UpdateCustomer(Schema):
    '''
    Args:
        email: Contact corporate e-mail address.
    '''
    name:        str
    nif:         str
    address:     str
    country:     str # TODO: validator
    province:    str
    city:        str
    postal_code: int
    phone:       str
    email:       EmailStr


class CreateCustomer(UpdateCustomer):
    pass


class Customer(CreateCustomer, DatedMixin, table=True):
    id: int = Field(primary_key=True)


class Application(Schema):
    name:    str = Field(primary_key=True)
    enabled: bool


class DeviceStatus(StrEnum):
    ACTIVE   = 'active'
    STALE    = 'stale'
    ARCHIVED = 'archived'


class UpdateDevice(Schema):
    '''
    Args:
        server: The device has a server role.
    '''
    config:   str
    status:   DeviceStatus
    server:   bool = False


class CreateDevice(UpdateDevice):
    pass


class Device(CreateDevice, DatedMixin, table=True):
    id:       UUID = Field(primary_key=True)
    customer: int = Field(foreign_key='customer.id')
