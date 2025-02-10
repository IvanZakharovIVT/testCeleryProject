from sqladmin import ModelView
from starlette.requests import Request

from wtforms.fields.simple import StringField

from database import User, SquareInfo
from infrastructure.utils.user_utils import hash_password


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.full_name, User.user_type]
    form_excluded_columns = [User.password]
    form_extra_fields = {
        "new_password": StringField("New Password", description="Leave blank if no change")
    }

    async def on_model_change(self, data: dict, model: User, is_created: bool, request: Request) -> None:
        """
        Hash the password before saving the model.
        """
        # Check if a new password was provided
        new_password = data.get("new_password")
        if new_password:
            model.password = hash_password(new_password)

        # Remove the "new_password" field from the data (it's not a database column)
        data.pop("new_password", None)

        # Call the parent method to save the model
        await super().on_model_change(data, model, is_created, request)


class SquareInfoAdmin(ModelView, model=SquareInfo):
    """Admin view for the SquareInfo model."""

    column_list = [SquareInfo.id, SquareInfo.original_value, SquareInfo.square_count, SquareInfo.squares, SquareInfo.time_of_calculation]
    column_searchable_list = [SquareInfo.original_value]
    column_sortable_list = [SquareInfo.id, SquareInfo.original_value, SquareInfo.square_count, SquareInfo.time_of_calculation]
    form_excluded_columns = [SquareInfo.squares]  # Exclude complex fields like JSON from editing if needed
    name = "Square Info"
    name_plural = "Square Infos"
