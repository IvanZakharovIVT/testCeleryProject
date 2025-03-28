import time
from decimal import Decimal

from src.serializers.square_calc import SquareResult


def sum_of_squares(n: int) -> SquareResult:
    start_time = time.time()
    limit = round(n**0.5 // 1)
    result_count = {}
    for i in range(limit, 0, -1):
        sq_list = []
        n_buffer = n
        sq_list.append(i)
        n_buffer -= i ** 2
        while True:
            if not n_buffer:
                result_count[len(sq_list)] = sq_list
                break
            similar_sq = round(n_buffer**0.5 // 1)
            sq_list.append(similar_sq)
            n_buffer -= similar_sq**2
    time_score = time.time() - start_time
    print("--- %s seconds ---" % (time.time() - start_time))
    sq = SquareResult(
        original_value=n,
        square_count=min(result_count),
        time_of_calculation=Decimal(time_score),
        squares=result_count[min(result_count)]

    )
    return sq
