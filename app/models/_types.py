from enum import Enum
from uuid import UUID
from pydantic import EmailStr

class StrEnum(str, Enum):
    __str__ = str.__str__


__all__ = ['EmailStr', 'UUID']
