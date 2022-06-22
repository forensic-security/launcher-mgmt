from ._router import APIRouter, Depends, crud_router

from ..models.user import AccessToken, User, CreateUser, UpdateUser
from .dependencies.auth import get_access_token, get_current_active_user, OAuth2PasswordRequestForm

user = crud_router(User, CreateUser, UpdateUser, delete=False)
auth = APIRouter()


@auth.post('/login', response_model=AccessToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await get_access_token(form_data)


# @user.get('/me', response_model=User)
# async def get_user_info(user: User = Depends(get_current_active_user)):
#     return user



# Good point, @ChuckMoe! It's truly impressive the amount of boilerplate that can be reduced with this SQLModel and FastAPI-CRUDRouter.
