import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.interfaces.api import api_v1_router

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

app.include_router(api_v1_router.router)
