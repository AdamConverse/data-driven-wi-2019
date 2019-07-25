import os
import sys
import time
from datetime import datetime

def my_task():
  start_time = datetime.now()
  time.sleep(3)
  return { "start_time": start_time, "end_time": datetime.now() }