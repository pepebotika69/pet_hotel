RUFF_VERSION = 0.9.10
RUFF_DOCKER = docker run --rm -v $(PWD):/code -w /code ghcr.io/astral-sh/ruff:$(RUFF_VERSION)
WEB = docker compose run --rm -u "$$(id -u):$$(id -g)" web

lint:
	$(RUFF_DOCKER) check .

lint-fix:
	$(RUFF_DOCKER) check --fix .

format:
	$(RUFF_DOCKER) format .

format-check:
	$(RUFF_DOCKER) format --check .

fix:
	$(RUFF_DOCKER) check --fix .
	$(RUFF_DOCKER) format .

makemessages:
	mkdir -p apps/embassy/locale
	$(WEB) python manage.py makemessages -l es -i staticfiles

compilemessages:
	$(WEB) python manage.py compilemessages
