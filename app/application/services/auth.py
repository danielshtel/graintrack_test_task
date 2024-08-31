from datetime import datetime, timezone, timedelta

import bcrypt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dependencies.auth import validate_token
from app.application.dependencies.db import get_db_session
from app.application.dto.auth import AuthResponse, Token
from app.core.config import settings
from app.core.constants import TokenType
from app.domain.models import User

UTF_8_ENCODING= 'utf-8'

security_scheme = HTTPBearer()

def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(UTF_8_ENCODING), salt)
    return hashed_password.decode(UTF_8_ENCODING)


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(UTF_8_ENCODING), password_hash.encode(UTF_8_ENCODING))


async def get_token_from_headers(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> str:
    token = credentials.credentials

    return token


async def verify_token(
    token: str = Depends(get_token_from_headers),
    session: AsyncSession = Depends(get_db_session)
) -> dict:
    claims = await validate_token(token, session)
    return claims


def generate_token(user: User, token_type: str) -> str:
    claims = {
        'sub': str(user.id),
        'token_type': token_type,
    }

    if token_type == TokenType.ACCESS_TOKEN:
        secret = settings.ACCESS_TOKEN_SECRET
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == TokenType.REFRESH_TOKEN:
        secret = settings.REFRESH_TOKEN_SECRET
        expiration_time = datetime.now(timezone.utc) + timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS)

    claims['exp'] = expiration_time

    token = jwt.encode(
        claims=claims,
        key=secret,
        algorithm=settings.JWT_ALGORITHM
    )
    return token


def create_auth_response(user: User) -> AuthResponse:
    access_token = generate_token(user, TokenType.ACCESS_TOKEN)
    refresh_token = generate_token(user, TokenType.REFRESH_TOKEN)
    token = Token(access_token=access_token, refresh_token=refresh_token)
    auth_response = AuthResponse(token=token)
    return auth_response