from enum import StrEnum


class TokenType(StrEnum):
    ACCESS_TOKEN = 'ACCESS_TOKEN'
    REFRESH_TOKEN = 'REFRESH_TOKEN'


class ErrorMessage(StrEnum):
    TOKEN_IS_INVALID = 'Token is invalid'
    INVALID_CREDENTIALS = 'Invalid credentials'