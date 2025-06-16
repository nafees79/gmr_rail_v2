import redis
from config import config

class Redisinstance:
    
    def __init__(self):
        self.instance = redis.Redis(host=config.DATABASE_HOST, 
                                    port=6379, 
                                    decode_responses=True, 
                                    password=config.REDIS_CREADS, 
                                    )
        
    def cache(self):
        '''
        write your cache function here
        '''
        pass
        

RedisConn = Redisinstance()