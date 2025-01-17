import time


def sum_of_squares(n):
    start_time = time.time()
    limit = round(n**0.5 // 1)
    result_list = []
    for i in range(limit, 0, -1):
        sq_list = []
        n_buffer = n
        sq_list.append(i)
        n_buffer -= i ** 2
        while True:
            if not n_buffer:
                result_list.append(len(sq_list))
                break
            similar_sq = round(n_buffer**0.5 // 1)
            sq_list.append(similar_sq)
            n_buffer -= similar_sq**2
    print("--- %s seconds ---" % (time.time() - start_time))
    return min(result_list)
