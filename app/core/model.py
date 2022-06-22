from typing import Any, Optional, TYPE_CHECKING
from datetime import datetime

from pydantic import BaseModel, SecretStr, validator, root_validator
from pydantic.fields import Undefined
from sqlmodel import SQLModel as _SQLModel, Column, DateTime, Relationship, Field as _Field, func
from sqlalchemy.orm import declared_attr

from .utils import snake_case

if TYPE_CHECKING:
    from sqlmodel.main import FieldInfo


# add a `unique` prop which creates a UNIQUE CONSTRAINT in the field
def Field(default: Any=Undefined, **kwargs) -> 'FieldInfo':
    unique = kwargs.pop('unique', False)
    if unique is True:
        sa_column_kwargs = kwargs.get('sa_column_kwargs', {})
        sa_column_kwargs['unique'] = True
        sa_column_kwargs.setdefault('index', False)
        kwargs['sa_column_kwargs'] = sa_column_kwargs
    return _Field(default, **kwargs)


# Workaround for serializing properties and allowing calculated fields in create and update schemas.
# https://github.com/samuelcolvin/pydantic/issues/935#issuecomment-753321423
class Schema(_SQLModel):

    @classmethod
    def get_props(cls):
        attrs = {prop: getattr(cls, prop) for prop in dir(cls) if prop[0:2] != '__'}
        return {
            name: attr for name, attr in attrs.items()
            if isinstance(attr, property) and name not in ('__values__', 'fields')
        }
        # return {name: attr for name, attr in attrs.items() if isinstance(attr, property)}

    def dict(self, *args, **kwargs):
        try:
            update = {name: attr.fget(self) for name, attr in self.get_props().items()}
        except TypeError:
            update = {}
        return {**super().dict(*args, **kwargs), **update}

    class Config:
        anystr_strip_whitespace = True
        smart_union = True
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }

    @declared_attr
    def __tablename__(cls) -> str:
        return snake_case(cls.__name__)


class CreatedMixin(BaseModel):
    created: datetime = Field(default_factory=func.now)
    # created: Optional[datetime] = Field(
    #     sa_column=Column(
    #         DateTime,
    #         default=func.now(),
    #         nullable=False,
    #     )
    # )


class DatedMixin(CreatedMixin):
    updated: datetime = Field(
        default_factory=func.now,
        sa_column_kwargs={'onupdate': func.now()}
    )
    # updated: Optional[datetime] = Field(
    #     sa_column=Column(
    #         DateTime,
    #         default=func.now(),
    #         onupdate=func.now(),
    #         nullable=False,
    #     )
    # )
