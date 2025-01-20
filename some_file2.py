import redis

from tasks import app

inspector = app.control.inspect()

r = redis.Redis(host='localhost', port=6379, db=0)
print(r.ping())

# Get scheduled tasks
scheduled_tasks = inspector.scheduled()

# Get active tasks  
active_tasks = inspector.active()

# Get reserved tasks (tasks claimed by workers)
reserved_tasks = inspector.reserved()