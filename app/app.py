from __future__ import print_function
import os
import sys
import json
import time
from flask import Flask, request, abort, jsonify, render_template, current_app
from redis import Redis
from rq import Queue
from __init__ import create_app, redis_url
import tasks

app = create_app()
url = redis_url()
conn = None
if os.environ.get('REDIS_URL') == "redis":
  conn = Redis(host='redis', port=6379)
else:
  conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)
q = Queue(connection=conn)

@app.route('/', methods=['GET'])
def index():
  app.logger.debug("/ request recieved")
  return "Hello World!"

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 8080))
  host = app.config["HOST"]
  app.run(host=host, port=port, threaded=True)
