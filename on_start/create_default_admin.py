from config import settings
from database import User
from infrastructure.enums.user_type import UserType
from infrastructure.repository.users import UserRepository
from infrastructure.utils.user_utils import hash_password, convert_name_to_username

async def create_admin_user(db_session):
    full_name = settings.DEFAULT_ADMIN_FULL_NAME
    username = convert_name_to_username(full_name)
    existed_user = await UserRepository(db_session).get_user_by_username(username)
    if not existed_user:
        password = hash_password(settings.DEFAULT_ADMIN_PASSWORD)
        user = User(
            full_name=full_name,
            username=username,
            user_type=UserType.ADMIN.value,
            password=password,
        )
        db_session.add(user)
