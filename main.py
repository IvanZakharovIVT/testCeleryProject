from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import ORIGINS
from routers.square_task import router as task_router


app = FastAPI(
    root_path="/api",  # This should match your API base URL
    openapi_url="/openapi.json",
    title="mpayments",
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
