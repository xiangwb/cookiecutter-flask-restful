FLASK_ENV=development
FLASK_APP={{cookiecutter.app_name}}.app:create_app
SECRET_KEY=changeme
DATABASE_URI=mongodb://localhost:27017/{{cookiecutter.app_name}}
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
