from sqladmin import ModelView
from starlette.requests import Request

from wtforms.fields.simple import StringField

from database import User, SquareInfo
from infrastructure.utils.user_utils import hash_password


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.full_name, User.user_type, User.password]
    form_create_rules  = ['username', 'full_name', 'user_type', 'password']
    form_edit_rules  = ['username', 'full_name', 'user_type']
    form_extra_fields = {
        "new_password": StringField("New Password", description="Leave blank if no change")
    }
    form_overrides = {"new_password": str}  # Define the type of the custom field
    form_widget_args = {
        "new_password": {
            "type": "password",  # Render the field as a password input
        }
    }

    async def on_model_change(self, data: dict, model: User, is_created: bool, request: Request) -> None:
        if is_created:
            data['password'] = hash_password(data.get('password'))
        await super().on_model_change(data, model, is_created, request)


class SquareInfoAdmin(ModelView, model=SquareInfo):
    column_list = [SquareInfo.id, SquareInfo.original_value, SquareInfo.square_count, SquareInfo.squares, SquareInfo.time_of_calculation]
    column_searchable_list = [SquareInfo.original_value]
    column_sortable_list = [SquareInfo.id, SquareInfo.original_value, SquareInfo.square_count, SquareInfo.time_of_calculation]
    form_excluded_columns = [SquareInfo.squares]
    name = "Square Info"
    name_plural = "Square Infos"
