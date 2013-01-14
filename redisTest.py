import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r['foo'] = 'bar'

print r['foo']