from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from ..core.db import get_db
from ..core.utils import spinal_case
from ..core.router import SQLModelCRUDRouter
from .dependencies.auth import get_current_active_user


if TYPE_CHECKING:
    from typing import Optional, List, Callable, Union, Literal
    from pydantic import BaseModel
    from sqlmodel import SQLModel


def crud_router(
    schema:       'SQLModel',
    create:       'Union[BaseModel, None, Literal[False]]' = None,
    update:       'Union[BaseModel, None, Literal[False]]' = None,
    prefix:       'Optional[str]' = None,
    dependencies: 'Optional[List[Callable]]' = None,
    delete:       bool = True,
    paginate:     int = 25,
    **kwargs,
):
    if dependencies is None:
        dependencies = [get_current_active_user]
    if create is False:
        kwargs['create_route'] = False
    if update is False:
        kwargs['update_route'] = False
    if delete is False:
        kwargs['delete_one_route'] = False

    return SQLModelCRUDRouter(
        schema=schema,
        create_schema=create,
        update_schema=update,
        db=get_db,
        prefix=prefix or spinal_case(schema.__name__),
        delete_all_route=False,
        dependencies=[Depends(d) for d in dependencies or []],
        paginate=paginate,
        **kwargs,
    )

__all__ = ['crud_router', 'Depends', 'APIRouter']
