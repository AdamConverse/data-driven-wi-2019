import os
import sys
import time
from flask import jsonify
from datetime import datetime

def my_task():
  time = datetime.now()
  time.sleep(3)
  return jsonify({ "start_time": time, "end_time": datetime.now() })