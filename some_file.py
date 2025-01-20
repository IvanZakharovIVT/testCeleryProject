import redis

from tasks import me_reverse, app


result = me_reverse.delay("Ivan Zakharov")

print(result.ready())
try:
    print(result.get(timeout=5))
except redis.exceptions.TimeoutError:
    print("Timeout occurred while retrieving result")
