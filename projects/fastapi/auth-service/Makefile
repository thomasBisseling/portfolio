ENV = venv
BIN = $(ENV)/bin
PYTHON_VERSION = 3.12
PYTHON = $(BIN)/python

APP_CONTAINER := docker compose run -i --rm api


.PHONY: secrets
secrets:
	# The flag -n errors when files already exist in the destination. It's not a harmful errors, however it does
    # prevent other commands from running. By adding a dash to cp (-cp), the error is ignored.
	-cp -r -n secrets-example/. secrets

$(ENV):
	$(shell which python$(PYTHON_VERSION)) -m venv $(ENV)
	# Fallback if specific version not found
	if [ ! -d "$(ENV)" ]; then \
		python3 -m venv $(ENV); \
	fi

requirements.txt.done: $(ENV)
	$(PYTHON) -m pip install --upgrade pip wheel setuptools
	$(PYTHON) -m pip install -r src/requirements/development.txt
	touch $@

up: secrets requirements.txt.done migrate
	docker compose up -d

down: secrets requirements.txt.done
	docker compose down --remove-orphans

.SILENT: attach
attach: secrets requirements.txt.done
	docker compose logs api --tail=25
	docker compose attach api

shell: secrets requirements.txt.done
	docker compose run -i --rm api bash

logs: secrets requirements.txt.done
	docker compose logs api -f

rebuild: secrets requirements.txt.done
	rm -rf $(ENV) && $(shell which python$(PYTHON_VERSION)) -m venv $(ENV)
	rm -rf requirements.txt.done && $(PYTHON) -m pip install -r src/requirements/development.txt
	# Rebuild the container and remove all volumes
	docker compose up -d --build --force-recreate

migrate: secrets requirements.txt.done
	$(APP_CONTAINER) make migrate ARGS="$(ARGS)"

createmigration: secrets requirements.txt.done
	$(APP_CONTAINER) make createmigration ARGS="$(ARGS)"

fix-codestyle: secrets requirements.txt.done
	$(APP_CONTAINER) make fix-codestyle

test: secrets requirements.txt.done
	$(APP_CONTAINER) make test ARGS="$(ARGS)"

docs: secrets requirements.txt.done
	$(APP_CONTAINER) make docs ARGS="$(ARGS)"

clean: secrets requirements.txt.done
	docker compose down --remove-orphans --volumes

.PHONY: requirements
requirements: secrets
	$(APP_CONTAINER) make requirements

pytest-debug: secrets requirements.txt.done
	$(APP_CONTAINER) make pytest-debug ARGS="$(ARGS)"
