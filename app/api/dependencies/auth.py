from typing import Optional
from datetime import datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from ...exceptions import AuthenticationError, ContentError
from ...config import settings
from ...logger import log
from ...models.user import User, AccessToken, TokenData, PSWD_CTX
from ...core.db import get_db


oauth2 = OAuth2PasswordBearer(tokenUrl='login')


async def get_user(username: str):
    return (await anext(get_db())).query(User).filter(User.username == username).first()


async def authenticate_user(username: str, password: str) -> Optional[User]:
    if (user := await get_user(username)):
        if PSWD_CTX.verify(password, user.password):
            return user


async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> AccessToken:
    # XXX: added lower() to validate email addresses (TODO: manage in model)
    if (user := await authenticate_user(form_data.username.lower(), form_data.password)) is None:
        raise AuthenticationError('Invalid username or password')

    token_data = {
        'sub': f'username:{user.username}',
        'exp': datetime.utcnow() + settings.token_exp_secs,
    }

    access_token = jwt.encode(
        token_data,
        settings.jwk.get_secret_value(),
        algorithm=settings.jws_algorithm,
    )

    return AccessToken(
        username=user.username,
        full_name=user.username,   # FIXME
        access_token=access_token,
        token_type='bearer',
        roles=['user'],
        id=2,
    )


async def get_current_user(token: str = Depends(oauth2)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.jwk.get_secret_value(),
            algorithms=[settings.jws_algorithm],
        )
        if (subject := payload.get('sub')) is None:
            raise AuthenticationError
        try:
            token_data = TokenData.parse_raw(subject)
        except ValueError:
            raise ContentError(f'Invalid subject: {subject!r}')

        if (user := get_user(token_data.username)) is None:
            raise AuthenticationError
    except (JWTError, AuthenticationError):
        raise AuthenticationError('Invalid credentials') from None
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not (user := await current_user).enabled:
        raise AuthenticationError('Inactive user')
    return user
