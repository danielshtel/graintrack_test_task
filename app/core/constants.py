from enum import StrEnum


class TokenType(StrEnum):
    ACCESS_TOKEN = 'ACCESS_TOKEN'
    REFRESH_TOKEN = 'REFRESH_TOKEN'


class ErrorMessage(StrEnum):
    # Auth
    TOKEN_IS_INVALID = 'Token is invalid'
    INVALID_CREDENTIALS = 'Invalid credentials'
    NO_PERMISSIONS = 'You have no permissions to do this action'

    # User
    USER_IS_ALREADY_REGISTERED = 'User is already registered'
    USER_NOT_FOUND = 'User not found'

    # Category
    CATEGORY_NOT_FOUND = 'Category not found'

    # Product
    PRODUCT_NOT_FOUND = 'Product not found'
