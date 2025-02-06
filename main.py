import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.db_config import get_session
from config.settings import ORIGINS
from on_start.create_default_admin import create_admin_user
from routers.exceptions.users import setup_user_handlers
from routers.square_task import router as task_router
from routers.square_calculation import router as calculation_router
from routers.users import router as user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app1: FastAPI):
    async for db_session in get_session():
        await create_admin_user(db_session)
        await db_session.flush()
        await db_session.commit()
    yield

app = FastAPI(
    root_path="/api",  # This should match your API base URL
    openapi_url="/openapi.json",
    title="Squares calculation",
    version="1.0.0",
    openapi_version="3.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(calculation_router)
app.include_router(user_router)

setup_user_handlers(app)
