import os
import random

from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/neilmcb/testing-goat-book.git'

def deploy():
	site_folder = f'/home/{env.user}/sites/{env.host}'
	run(f'mkdir -p {site_folder}')
	with cd(site_folder):
		_get_latest_source()
		_update_venv()
		_get_or_create_dotenv()
		_update_static_files()
		_update_database()


def _get_latest_source():
	if exists('.git'):
		run('git fetch')
	else:
		run(f'git clone {REPO_URL} .')
	
	# Overwrite any local changes
	current_commit = local('git log -n 1 --format=%H', capture=True)
	run(f'git reset --hard {current_commit}')


def _update_venv():
	if not exists('venv/bin/pip'):
		run(f'python3 -m venv venv')
	run('./venv/bin/pip install -r requirements.txt')


def _get_or_create_dotenv():
	append('.env', f'SITENAME={env.host}')
	
	current_contents = run('cat .env')
	if 'DJANGO_SECRET_KEY' not in current_contents:
		new_secret = ''.join(random.SystemRandom().choices(
			'abcdefghijklmnopqrstuvwxyz0123456789', k=50
		))
		append('.env', f'DJANGO_SECRET_KEY={new_secret}')
	if 'DJANGO_EMAIL_PASSWORD' not in current_contents:
		append('.env', f'DJANGO_EMAIL_PASSWORD={os.environ.get("DJANGO_EMAIL_PASSWORD")}')


def _update_static_files():
	run('DJANGO_DEBUG=true ./venv/bin/python manage.py collectstatic --noinput')


def _update_database():
	run('DJANGO_DEBUG=true ./venv/bin/python manage.py migrate --noinput')
 
