SHELL := /bin/sh
WORKDIR = $(shell basename "$(shell pwd)")
UPGRADE = yes

# Ensure that the list contains only phony targets
PHONY_TARGETS := $(filter-out $(.PHONY), $(PHONY_TARGETS))

APP_CONTAINER := docker compose run -i --rm api

.env:
	touch .env

.PHONY: secrets
secrets:
	# The flag -n errors when files already exist in the destination. It's not a harmful errors, however it does
    # prevent other commands from running. By adding a dash to cp (-cp), the error is ignored.
	-cp -r -n secrets-example/. secrets

up: secrets .env migrate
	docker compose up -d

down: secrets .env
	docker compose down --remove-orphans

.SILENT: attach
attach: secrets .env
	docker logs "$(WORKDIR)-api" --tail=25
	docker attach "$(WORKDIR)-api"

shell: secrets .env
	docker compose exec api -it bash --rm

logs: secrets .env
	docker compose logs api -f

rebuild: secrets .env
	docker compose up -d --build --force-recreate

migrate: secrets .env
	$(APP_CONTAINER) make migrate

makemigrations: secrets .env
	$(APP_CONTAINER) make makemigrations

createsuperuser: secrets .env
	$(APP_CONTAINER) make createsuperuser

fix-codestyle: secrets .env
	$(APP_CONTAINER) make fix-codestyle

test: secrets .env
	$(APP_CONTAINER) make test

docs: secrets .env
	$(APP_CONTAINER) make docs

clean: secrets .env
	docker compose down --remove-orphans --volumes

.PHONY: requirements
requirements: secrets .env
	$(APP_CONTAINER) make requirements