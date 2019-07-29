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
  app.logger.info("/ request recieved")
  return "Hello World!"

@app.route('/dropbox', methods=['GET'])
def dropbox():
  app.logger.info("Dropbox webhook challenge: {}".format(request.args.get('challenge')))
  return request.args.get('challenge')

@app.route('/dropbox-test', methods=['GET'])
@app.route('/dropbox', methods=['POST'])
def dropbox_update():
  app.logger.info("Webhook recieved")
  q.enqueue(tasks.post_to_slack)
  return ""

@app.route('/test-job', methods=['GET'])
def test_job():
  app.logger.info("/test-job request recieved")
  job = q.enqueue(tasks.my_task)

  log = "Test Job Started. job_id: {}".format(job.id)
  app.logger.info(log)
  return log

@app.route('/job/<job_id>', methods=['GET'])
def job_id(job_id):
  job = q.fetch_job(job_id)

  return jsonify({"data": job.result})

@app.route('/run-simulations/<month>/<date>/<year>', methods=['GET'])
def run_simulations(month, date, year):
  date = "{}/{}/{}".format(month, date, year)
  job = q.enqueue(tasks.run_simulations, date)
  app.logger.info("Simulation Started. job_id: {}".format(job.id))
  return "Simulation Started. \njob_id: {}".format(job.id)

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 8080))
  host = app.config["HOST"]
  app.run(host=host, port=port, threaded=True)
