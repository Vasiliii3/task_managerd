MANAGE := poetry run python manage.py

install:
	poetry install

dev:
	@poetry runserver

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

selfcheck:
	poetry check

check: selfcheck test lint

lint:
	poetry run flake8 task_manager

.PHONY: install test lint selfcheck check build

migrate:
	@poetry makemigrations
	@poetry migrate

messages:
		poetry run django-admin makemessages -l ru
compilemess:
		poetry run django-admin compilemessages