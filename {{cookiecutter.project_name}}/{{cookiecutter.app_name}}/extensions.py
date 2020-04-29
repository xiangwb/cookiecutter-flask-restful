"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
{%- if cookiecutter.use_celery == "yes" %}
from celery import Celery
{%- endif %}
{%- if cookiecutter.use_limiter == "yes" %}
from flask_limiter.util import get_remote_address
{%- endif %}

from {{cookiecutter.app_name}}.commons.apispec import APISpecExt

from {{cookiecutter.app_name}}.loggers import Logger


jwt = JWTManager()
ma = Marshmallow()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
{%- if cookiecutter.use_celery == "yes" %}
celery = Celery()
{%- endif %}
logger = Logger()
{%- if cookiecutter.use_limiter == "yes" %}
limiter = Limiter(key_func=get_remote_address, default_limits=["10000/day, 2000/minute, 1000/second"])
{%- endif %}