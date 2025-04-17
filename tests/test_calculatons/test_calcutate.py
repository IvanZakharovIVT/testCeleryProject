import pytest
from src.infrastructure.services.calculate_squares import sum_of_squares

params_calc=(
    (12345677, [371, 3494]),
    (12345673, [259, 3504, 24]),
    (12345675, [115, 3511, 73])
)

@pytest.fixture(params=params_calc)
def f_wrapper_function(request):
    '''fixture: Возвращает объект'''
    yield request.param
    print('fixture: Завершение созданного объекта')

def test_calculate_squares(f_wrapper_function):
  calc_result = sum_of_squares(f_wrapper_function[0])
  assert calc_result.squares == f_wrapper_function[1]
