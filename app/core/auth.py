from datetime import datetime, timezone, timedelta

import bcrypt
from jose import jwt

from app.application.models import User
from app.core.config import settings
from app.core.constants import TokenType
from app.domain.dto.auth import AuthResponse, Token

UTF_8_ENCODING= 'utf-8'


def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(UTF_8_ENCODING), salt)
    return hashed_password.decode(UTF_8_ENCODING)


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(UTF_8_ENCODING), password_hash.encode(UTF_8_ENCODING))


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