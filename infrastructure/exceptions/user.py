class UserAuthorizationError(Exception):
    def __init__(self, username: str):
        self.username = username

    @property
    def error_message(self) -> str:
        return "Неверно указан логин или пароль"