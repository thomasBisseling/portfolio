#!/bin/sh

ansible-galaxy install -r requirements.yml
ansible-playbook -i inventory/local.yml site.yml