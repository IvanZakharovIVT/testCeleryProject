import pytest
from src.infrastructure.utils.user_utils import convert_name_to_username

params_calc = (
    ("Hello There my friend 123!!!", "hello_there_my_friend_123"),
    ("_=5F3hh", "_5f3hh"),
)


@pytest.fixture(params=params_calc)
def f_wrapper_function(request):
    """fixture: Возвращает объект"""
    yield request.param
    print("fixture: Завершение созданного объекта")


def test_convert_name_to_username(f_wrapper_function):
    calc_result = convert_name_to_username(f_wrapper_function[0])
    assert calc_result == f_wrapper_function[1]
