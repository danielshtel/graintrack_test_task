from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import TokenType, ErrorMessage

security_scheme = HTTPBearer()

async def get_token_from_headers(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> str:
    token = credentials.credentials

    return token

async def validate_token(token: str, session: AsyncSession) -> dict:

    try:
        token_type = jwt.get_unverified_claims(token)['token_type']
    except JWTError:
        raise JWTError(ErrorMessage.TOKEN_IS_INVALID)

    if token_type == TokenType.ACCESS_TOKEN:
        secret = settings.ACCESS_TOKEN_SECRET
    elif token_type == TokenType.REFRESH_TOKEN:
        secret = settings.REFRESH_TOKEN_SECRET

    try:
        claims = jwt.decode(token=token,
                            key=secret,
                            algorithms=settings.JWT_ALGORITHM)
    except ExpiredSignatureError:
        raise JWTError(ErrorMessage.TOKEN_IS_INVALID)
    return claims
