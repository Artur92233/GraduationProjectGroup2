"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-15899.crce175.eu-north-1-1.ec2.redns.redis-cloud.com',
    port=15899,
    decode_responses=True,
    username="default",
    password="EkcK1lAupq2OT6T0LcBoxbZKrUXGeVHb",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

