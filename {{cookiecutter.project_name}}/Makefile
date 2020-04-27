.PHONY: init build run test tox pyc

init:  build run
	docker-compose exec web {{cookiecutter.app_name}} db upgrade
	docker-compose exec web {{cookiecutter.app_name}} init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

test:
{%- if cookiecutter.use_celery == "yes"%}
	docker-compose stop celery # stop celery to avoid conflicts with celery tests
	docker-compose start redis # ensuring both redis are started
{%- endif %}
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e test
{%- if cookiecutter.use_celery == "yes"%}
	docker-compose start celery
{%- endif %}

tox:
{%- if cookiecutter.use_celery == "yes"%}
	docker-compose stop celery # stop celery to avoid conflicts with celery tests
	docker-compose start redis # ensuring both redis are started
{%- endif %}
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e {{ cookiecutter.tox_python_env }}
{%- if cookiecutter.use_celery == "yes"%}
	docker-compose start celery
{%- endif %}

lint:
	docker-compose run web tox -e lint

pyc:
	python3 generate_deploy_pyc.py