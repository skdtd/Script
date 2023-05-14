import json
import time

import redis

rds = redis.Redis(host="localhost", port=16461)
rds.zadd("data", {"123": 1684082609086})

print()
rds.set("show", str())
print(json.dumps(rds.get("show").decode("utf-8")))