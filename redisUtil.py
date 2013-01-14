import redis
import weiboUtil

class redisUtil:
	r = None
	
	def _init_:
		r = redis.Redis(host='localhost', port=6379, db=0)
	
	def getRedis()
		return r
		
	def getRedisIdByScreenName(screen_name, key_name):
		return 'screen_name$' + screen_name + '$' + key_name


	def getRedisIdByUserId(user_id, key_name):
		return 'user_id$' + str(user_id) + '$' + key_name	
		
	