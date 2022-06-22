from typing import Literal, Optional
from datetime import timedelta
from pathlib import Path
import os

from pydantic import BaseSettings, SecretStr

ENVFILE = Path(__file__).resolve().parents[1] / '.env'

JwsAlgorithm = Literal[
    'HS256', 'HS384', 'HS512',  # HMAC using SHA-x hash algorithm
    'RS256', 'RS384', 'RS512',  # RSASSA using SHA-x hash algorithm
    'ES256', 'ES384', 'ES512',  # ECDSA using SHA-x hash algorithm
]


class Postgres(BaseSettings):
    user:     str
    password: SecretStr
    host:     str
    port:     str
    db:       str

    @property
    def uri(self) -> str:
        return (
            f'postgresql://{self.user}:{self.password.get_secret_value()}'
            f'@{self.host}:{self.port}/{self.db}'
        )

    class Config:
        env_file = ENVFILE
        env_prefix = 'postgres_'


class Settings(BaseSettings):
    '''
    Args:
        jwk: JSON Web Key.
        jws_algorithm: JSON Web Signature algorithm.
        token_exp_secs: seconds until token expiration.
    '''
    loglevel:       Optional[str] = 'info'
    postgres:       Postgres = Postgres()
    jwk:            SecretStr
    jws_algorithm:  JwsAlgorithm = 'HS256'
    token_exp_secs: timedelta

    class Config:
        env_file = ENVFILE
        env_prefix = 'app_'
        fields = {'loglevel': {'env': 'loglevel'}}

    @property
    def db_uri(self) -> str:
        return self.postgres.uri


try:
    settings = Settings()
except:
    raise RuntimeError(os.environ)
