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

ORIGINS = json.loads(os.getenv("ORIGINS", '["*"]'))

BASE_ML_API_URL = os.getenv('BASE_ML_API_URL', '')

PROJECT_DIR = Path.cwd()
TEMPLATE_FILE_PATH = PROJECT_DIR / os.getenv("TEMPLATE_FILE_PATH", 'media_files/templates/')
BUFFER_FILE_PATH = PROJECT_DIR / os.getenv("BUFFER_FILE_PATH", 'media_files/buffer_files/')

INVOICE_TEMPLATE = TEMPLATE_FILE_PATH / "invoice_template.docx"
CONTRACT_TEMPLATE = TEMPLATE_FILE_PATH / "contract_template.docx"

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "")

MAX_TASK_EXECUTION_TIME = 6 * 60
