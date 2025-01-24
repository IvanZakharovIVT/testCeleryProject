from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import ORIGINS
from routers.exceptions.users import setup_user_handlers
from routers.square_task import router as task_router
from routers.square_calculation import router as calculation_router
from routers.users import router as user_router


app = FastAPI(
    root_path="/api",  # This should match your API base URL
    openapi_url="/openapi.json",
    title="Squares calculation",
    version="1.0.0",
    openapi_version="3.1.0"
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
