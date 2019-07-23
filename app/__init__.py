import os
import sys
import logging
import urlparse
from flask import Flask, request, abort
from dotenv import load_dotenv, find_dotenv
from config.default import Config, Development, Production


def create_app():
    app = Flask(__name__)
    load_config(app)
    return app


def load_config(app):
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    on_heroku = os.environ.get('DYNO', None)
    if on_heroku is None:
        load_dotenv(find_dotenv())
        app.config.from_object(Development)
        app.logger.setLevel(logging.DEBUG)
    else:
        app.config.from_object(Production)
        app.logger.setLevel(logging.INFO)

def redis_url():
    load_dotenv(find_dotenv())

    redis_url = os.environ.get('REDIS_URL', "redis://127.0.0.1:6379")
    if not redis_url:
        raise RuntimeError('Redis url error. Ensure Redis is setup.')

    urlparse.uses_netloc.append('redis')
    url = urlparse.urlparse(redis_url)
    return url