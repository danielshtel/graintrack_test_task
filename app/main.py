import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError

from app.core.config import settings
from app.routes.api import api_v1_router

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info('Application startup')
    yield
    log.info('Application shutdown')


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    log.error(msg=exc)
    return JSONResponse({'detail': str(exc)}, status_code=500)


@app.exception_handler(ExpiredSignatureError)
async def expired_token_handler(request: Request, exc: ExpiredSignatureError):
    return JSONResponse({'detail': 'Token is expired'}, status_code=401)


@app.exception_handler(JWTError)
async def jwt_error_handler(request: Request, exc: JWTError):
    return JSONResponse({'detail': str(exc)}, status_code=401)


@app.exception_handler(JWTClaimsError)
async def jwt_claims_error_handler(request: Request, exc: JWTClaimsError):
    return JSONResponse({'detail': str(exc)}, status_code=401)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_message = errors[0]['msg']
    required_field = errors[0]['loc'][1]
    return JSONResponse({'detail': f"{error_message}: '{required_field}'"}, status_code=422)


app.include_router(api_v1_router.router)
