import os

class Config(object):
  DEBUG = False
  TESTING = False
  HOST = '127.0.0.1'

class Development(Config):
  DEBUG = True

class Production(Config):
  HOST = '0.0.0.0'
