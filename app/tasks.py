import os
import sys
from flask import jsonify
from datetime import datetime

def my_task():
  time = datetime.now()
  sleep(3)
  return jsonify({ "start_time": time, "end_time": datetime.now() })