from typing import Optional
from datetime import datetime, timedelta

from passlib.context import CryptContext

from ..core.model import Schema, CreatedMixin, DatedMixin, Field, Relationship, validator
from ._types import EmailStr

PSWD_CTX = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UpdateUser(Schema):
    password: str
    enabled:  bool

    @validator('password', pre=True)
    def hash_password(cls, v):
        return PSWD_CTX.hash(v)


class CreateUser(UpdateUser):
    username: EmailStr = Field(primary_key=True)

    @validator('username', pre=True)
    def username_to_lowercase(cls, v):
        return v.lower()


class User(CreateUser, DatedMixin, table=True):
    ...


class CreateUserAction(Schema):
    user:   str = Field(foreign_key='user.username')
    action: str   # TODO: enum
    params: Optional[str]


class UserAction(CreateUserAction, CreatedMixin, table=True):
    id: int = Field(primary_key=True)


class AccessToken(Schema):
    id:           int
    username:     str
    access_token: str  # TODO: hide
    token_type:   str
    roles:        list[str]


class TokenData(Schema):
    '''
    Los claims deben pasarse en formato `claim:value`. Ej.: `username:johndoe`.
    '''
    username: Optional[str] = None

    @classmethod
    def parse_raw(cls, content, **kwargs):
        return cls(**dict(claim.split(':') for claim in content.split()))


class JwtPayload(Schema):
    '''JWT (JSON Web Token) Payload.

    Args:
        exp: Expiration time.
        iat: Issued at.
        iss: Issuer. Principal that issued the JWT.
        sub: Subject.
    '''
    exp: datetime
    sub: str

    @property
    def iat(self) -> datetime:
        return datetime.utcnow()

    @property
    def iss(self) -> str:
        return 'Forensic and Security'

    @validator('exp', pre=True)
    def set_expiration(cls, v):
        if isinstance(v, (int, float)):
            return datetime.utcnow() + timedelta(v)
        elif isinstance(v, timedelta):
            return datetime.utcnow() + v
        return v
