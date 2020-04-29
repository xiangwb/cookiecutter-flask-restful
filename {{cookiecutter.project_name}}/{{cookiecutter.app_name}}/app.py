from flask import Flask
from mongoengine import connect

from {{cookiecutter.app_name}} import auth, api
from {{cookiecutter.app_name}}.extensions import jwt, apispec, logger
{%- if cookiecutter.use_celery == "yes"%}, celery{% endif%}{%- if cookiecutter.use_limiter == "yes"%}, limiter{% endif%}
from {{cookiecutter.app_name}}.request_handler import register_error_handler


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask("{{cookiecutter.app_name}}")
    app.config.from_object("{{cookiecutter.app_name}}.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app, cli)
    configure_apispec(app)
    register_request_handler(app)
    register_blueprints(app)
{%- if cookiecutter.use_celery == "yes" %}
    init_celery(app)
{%- endif %}

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    if cli is True:
        connect(host='mongodb://localhost:27017/{{cookiecutter.app_name}}_tmp')
    else:
        # 建立mongo的数据库连接，mongo的连接只需要connect就行
        connect(host=app.config['DATABASE_URI'])

    jwt.init_app(app)
    { % - if cookiecutter.use_limiter == "yes" %}
    limiter.init_app(app)
    { % endif %}
    logger.init_loggers(app)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)


def register_request_handler(app):
    """ 注册请求处理器 """

    # 注册错误请求处理函数
    register_error_handler(app)

    @app.before_request
    def before_request_callback():
        # FIXME: 添加你想要执行的操作
        pass

    @app.after_request
    def after_request_callback(response):
        # FIXME: 添加你想要执行的操作
        return response

{%- if cookiecutter.use_celery == "yes" %}


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
{%- endif %}
