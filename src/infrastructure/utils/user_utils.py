import hashlib
import random
import re
import string

from transliterate import translit

from src.config.settings import SPECIAL_SYMBOLS_TEMPLATE


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def generate_password() -> str:
    all_password_chars_list = list(string.ascii_letters + string.digits)
    random.shuffle(all_password_chars_list)
    return "".join(all_password_chars_list[0:8])


def convert_name_to_username(full_name: str) -> str:
    translit_full_name = translit(full_name.lower(), language_code='ru', reversed=True).strip()
    translit_full_name = translit_full_name.replace(" ", "_")
    translit_full_name = re.sub(SPECIAL_SYMBOLS_TEMPLATE, "", translit_full_name)
    translit_full_name = re.sub(r"\s+", "_", translit_full_name)
    return translit_full_name
