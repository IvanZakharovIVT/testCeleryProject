import json
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
DATABASE_A_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

DEFAULT_ADMIN_FULL_NAME = os.getenv('DEFAULT_ADMIN_FULL_NAME')
DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD')

SPECIAL_SYMBOLS_TEMPLATE = r"[^a-zA-Z0-9_\s]+"

ORIGINS = json.loads(os.getenv("ORIGINS", '["*"]'))

BASE_ML_API_URL = os.getenv('BASE_ML_API_URL', '')

PROJECT_DIR = Path.cwd()
TEMPLATE_FILE_PATH = PROJECT_DIR / os.getenv("TEMPLATE_FILE_PATH", 'media_files/templates/')
BUFFER_FILE_PATH = PROJECT_DIR / os.getenv("BUFFER_FILE_PATH", 'media_files/buffer_files/')

INVOICE_TEMPLATE = TEMPLATE_FILE_PATH / "invoice_template.docx"
CONTRACT_TEMPLATE = TEMPLATE_FILE_PATH / "contract_template.docx"

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "")
AUTH_TOKEN_TIMEDELTA = os.getenv('AUTH_TOKEN_TIMEDELTA', 60)
REFRESH_TOKEN_TIMEDELTA = os.getenv('REFRESH_TOKEN_TIMEDELTA', 60 * 2)

MAX_TASK_EXECUTION_TIME = 6 * 60

REDIS_HOST = os.getenv('REDIS_HOST', '')
REDIS_PORT = os.getenv('REDIS_PORT', '')
REDIS_PATH = CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
