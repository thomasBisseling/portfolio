# UPGRADE=no on command line overrides this.
UPGRADE=yes
ifdef UPGRADE_PACKAGE
	# Upgrade single package
	REQUIREMENTS_UPGRADE=--upgrade-package $(UPGRADE_PACKAGE)
else ifeq ($(UPGRADE),yes)
	# Upgrade all packages
	REQUIREMENTS_UPGRADE=--upgrade
else
	# Don't upgrade, only add/remove new/obsolete dependencies
	REQUIREMENTS_UPGRADE=--no-upgrade
endif

migrate:
	python main.py migrate $(ARGS)

createmigration:
	python main.py createmigration $(ARGS)

fix-codestyle:
	black service
	isort service

demodata:
	python main.py demodata $(ARGS)

security:
	bandit -c bandit.yaml -r service/

test: security
	pytest --cov-report=html --cov=service/ --cov-report=term-missing

docs:
	python manage.py generate_swagger -o -f yaml > docs/openapi.yaml

.PHONY: requirements
requirements:
	pip install --upgrade pip-tools
	rm -rf requirements/*.txt
	CUSTOM_COMPILE_COMMAND="make requirements" pip-compile $(REQUIREMENTS_UPGRADE) --resolver=backtracking --generate-hashes --output-file requirements/production.txt requirements/production.in
	CUSTOM_COMPILE_COMMAND="make requirements" pip-compile $(REQUIREMENTS_UPGRADE) --resolver=backtracking --generate-hashes --output-file requirements/development.txt requirements/development.in
	rm -rf *.egg-info

pytest-debug:
	 python3 -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 -m pytest $(ARGS)