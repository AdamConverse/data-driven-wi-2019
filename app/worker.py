import os
from redis import Redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from __init__ import redis_url

listen = ['high', 'default', 'low']
url = redis_url()
conn = None
if os.environ.get('REDIS_URL') == "redis":
  conn = Redis(host='redis', port=6379)
else:
  conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

if __name__ == '__main__':
  with Connection(conn):
    worker = Worker(map(Queue, listen))
    worker.work()