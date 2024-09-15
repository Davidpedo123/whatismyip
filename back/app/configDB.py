import redis
import os





PORT_REDIS = os.environ['PORT_REDIS']
HOST_REDIS = os.environ['HOST_REDIS']
PASSWD_REDIS = os.environ['PASSWD_REDIS']
redis_client = redis.StrictRedis(host=HOST_REDIS, port=PORT_REDIS, db=0, password=PASSWD_REDIS)