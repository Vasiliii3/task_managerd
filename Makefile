MANAGE := poetry run python manage.py

install:
	poetry install

dev:
	@$(MANAGE) runserver

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
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate

inter_one_rep:
		poetry run django-admin makemessages -l ru
inter_two_compil:
		poetry run django-admin compilemessages

test:
	@$(MANAGE) test
