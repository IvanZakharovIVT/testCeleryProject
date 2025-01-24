from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict, constr, field_validator

from infrastructure.enums.user_type import UserType
from infrastructure.utils.validate_fields import validate_spaces_str_field


class UserBase(BaseModel):
    full_name: constr(max_length=50)
    user_type: UserType

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("*", mode="before")
    @classmethod
    def validate_spaces_str_field(cls, value: Any):
        return validate_spaces_str_field(value)


class UserCreateResponse(BaseModel):
    id: int
    username: str
    password: str


class UserRetrieve(UserBase):
    id: int
    username: Optional[str] = None
    created_at: datetime

    class Config:
        from_attribute = True


class UserMeResponse(BaseModel):
    id: int
    username: str
    full_name: str
    user_type: str

    model_config = ConfigDict(from_attributes=True)


class UserCurrencyPosition(BaseModel):
    id: int
    full_name: str | None
    user_type: str
