from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.config.db_config import AsyncSessionLocal
from src.infrastructure.enums.user_type import UserType
from src.infrastructure.exceptions.user import UserAuthorizationError
from src.infrastructure.helpers.user import authenticate_and_get_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Handle user login."""
        form = await request.form()
        username, password = form["username"], form["password"]
        async with AsyncSessionLocal() as session:
            try:
                user = await authenticate_and_get_user(username, password, session)
                if user.user_type == UserType.ADMIN.value:
                    request.session.update({"token": "secret"})
                    return True
                return False
            except UserAuthorizationError:
                return False

    async def logout(self, request: Request) -> bool:
        """Handle user logout."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Check if the user is authenticated."""
        token = request.session.get("token")
        if not token:
            return RedirectResponse(url="/api/admin/login", status_code=302)

        return True  # Token validation logic can be added here if needed
