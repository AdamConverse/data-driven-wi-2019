from __future__ import print_function
import os
import sys
import json
import time
from flask import Flask, request, abort, jsonify, render_template, current_app
from __init__ import create_app, redis_url

app = create_app()

@app.route('/', methods=['GET'])
def index():
  app.logger.debug("/ request recieved")
  return "Hello World!"

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 8080))
  host = app.config["HOST"]
  app.run(host=host, port=port, threaded=True)
