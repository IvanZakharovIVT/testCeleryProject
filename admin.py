from sqladmin import ModelView

from database import User, SquareInfo


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.full_name, User.user_type]


class SquareInfoAdmin(ModelView, model=SquareInfo):
    """Admin view for the SquareInfo model."""

    column_list = [SquareInfo.id, SquareInfo.original_value, SquareInfo.square_count, SquareInfo.squares, SquareInfo.time_of_calculation]
    column_searchable_list = [SquareInfo.original_value]
    column_sortable_list = [SquareInfo.id, SquareInfo.original_value, SquareInfo.square_count, SquareInfo.time_of_calculation]
    form_excluded_columns = [SquareInfo.squares]  # Exclude complex fields like JSON from editing if needed
    name = "Square Info"
    name_plural = "Square Infos"
