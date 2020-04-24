"""Default configuration

Use env var to override
"""

from environs import Env

env = Env()

env.read_env(".flaskenv", recurse=False)

ENV = env("FLASK_ENV", "production")
DEBUG = ENV == "development"
SECRET_KEY = env("SECRET_KEY")

DATABASE_URI = env("DATABASE_URI")

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
{%- if cookiecutter.use_celery == "yes" %}
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND_URL")
{%- endif %}
