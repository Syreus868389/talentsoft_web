import os
import environ
import redis
from rq import Worker, Queue, Connection

env = environ.Env()
environ.Env.read_env()

listen = ['high', 'default', 'low']

redis_url = env('REDISTOGO_URL')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()