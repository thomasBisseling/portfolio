ENV = env
BIN = $(ENV)/bin
PYTHON_VERSION = 3.12
PYTHON = $(BIN)/python$(PYTHON_VERSION)

$(ENV):
	$(shell which python$(PYTHON_VERSION)) -m venv $(ENV)

requirements.txt.done: $(ENV) requirements.txt
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PYTHON) -m pip install -r requirements.txt
	touch $@

ansible.collections.done: requirements.txt.done
	$(BIN)/ansible-galaxy collection install -r ./requirements.yml
	touch $@

check: ansible.collections.done requirements.txt.done
	ansible-playbook -i inventories/local.yml site.yml --check -vvv

deploy: ansible.collections.done requirements.txt.done
	ansible-playbook -i inventories/local.yml site.yml --diff -vvv

grafana:
	docker compose up -d