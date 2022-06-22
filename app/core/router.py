from typing import Any, Callable, List, Optional, Type, Union

from fastapi import Depends
from sqlmodel import SQLModel
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_crudrouter.core._types import DEPENDENCIES
from fastapi_crudrouter.core.sqlalchemy import CALLABLE_LIST
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.orm import Session

from .db import paginate


class SQLModelCRUDRouter(SQLAlchemyCRUDRouter):
    def __init__(
        self,
        schema:           SQLModel,
        db:               Session,
        create_schema:    Optional[SQLModel] = None,
        update_schema:    Optional[SQLModel] = None,
        prefix:           Optional[str] = None,
        tags:             Optional[List[str]] = None,
        paginate:         Optional[int] = None,
        get_all_route:    Union[bool, DEPENDENCIES] = True,
        get_one_route:    Union[bool, DEPENDENCIES] = True,
        create_route:     Union[bool, DEPENDENCIES] = True,
        update_route:     Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        delete_all_route: Union[bool, DEPENDENCIES] = False,
        item_id:          Union[str, Callable[[str], str]] = 'item_id',
        **kwargs: Any,
    ):
        super().__init__(
            schema=schema,
            db=db,
            db_model=schema,
            create_schema=create_schema,
            update_schema=update_schema,
            prefix=prefix or schema.__tablename__,
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            delete_all_route=delete_all_route,
            **kwargs
        )
        if isinstance(item_id, str):
            self.item_id = item_id
        else:
            self.item_id = item_id(self.__class__.__name__)
