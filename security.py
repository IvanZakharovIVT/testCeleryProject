from authlib.jose.errors import BadSignatureError, ExpiredTokenError
from fastapi.security import HTTPBasic
from authlib.jose import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from fastapi_jwt import JwtAccessBearer
from starlette.requests import Request

from config.settings import JWT_SECRET_KEY
from infrastructure.exceptions.user import UserAuthorizationError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
access_security = JwtAccessBearer(secret_key=JWT_SECRET_KEY, auto_error=True)


class TokenEncode(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> dict:
        credentials = await super().__call__(request)
        token = str(credentials.credentials)
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY)
            payload.validate()
            return payload.get('subject', {})
        except ExpiredTokenError:
            raise HTTPException(status_code=401, detail="Срок действия токена закончился")
        except (UserAuthorizationError, BadSignatureError):
            raise HTTPException(status_code=401, detail="Invalid token or expired token")


basic_security = HTTPBasic()

token_security = TokenEncode()
