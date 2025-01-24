import re

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.enums.user_type import UserType
from infrastructure.exceptions.user import UserPermissionError, UserUniqueUsernameError
from infrastructure.repository.users import UserRepository
from infrastructure.utils.user_utils import convert_name_to_username, generate_password, hash_password
from serializers.users import UserBase, UserCreateResponse


class CreateUserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._user_repository = UserRepository(session)

    async def create(self, user: UserBase):
        if user.user_type == UserType.ADMIN.value:
            raise UserPermissionError(user.full_name)
        password = generate_password()
        new_username = convert_name_to_username(user.full_name)
        existed_user = await self._user_repository.get_user_by_username(new_username)
        if existed_user:
            raise UserUniqueUsernameError(new_username)
        new_password = hash_password(password)
        new_user = await self._user_repository.create(user)
        new_user.username = new_username
        new_user.password = new_password
        await self._user_repository.flush()
        return UserCreateResponse(id=new_user.id, username=new_username, password=password)

    @staticmethod
    def _validate_user_name(username: str):
        regexp = re.compile(r'^[^\W_][\w_\d-]+\w$')
        if not regexp.search(username):
            raise ValueError("Имя пользователя не прошло валидацию")
