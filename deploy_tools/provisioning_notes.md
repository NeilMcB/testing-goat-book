Provisioning a new site
=======================

## Reqired Packaces

* nginx
* Python 3.8
* virtualenv + pip
* Git

e.g. on Ubuntu:

	sudo apt update
	sudo apt install git nginx python3 python3-venv

## NGINX Virtual Host config

* see nginx.template.conf
* replace USER with e.g. ubuntu
* replace HOME with e.g. /home/USER
* replace DOMAIN with e.g. staging.neilmcblane.com

## Systemd service

* see gunicorn-systemd.template.service
* replace USER with e.g. ubuntu
* replace HOME with e.g. /home/USER
* replace DOMAIN with e.g. staging.neilmcblane.com

