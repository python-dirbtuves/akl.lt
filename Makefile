VENV_VERSION = 1.11.6


all: bin/django var/db.sqlite3

help:
	@echo 'make ubuntu     install the necessary system packages (requires sudo)'
	@echo 'make            set up the development environment'
	@echo 'make run        start the web server'
	@echo 'make testall    run the test suite, flake8, pylint, coverage'
	@echo 'make test       run project test suite'
	@echo 'make flake8     run flake8 on the source tree'
	@echo 'make pylint     run pylint on the source tree'
	@echo 'make clean      clean environment'
	@echo 'make cleanpyc   remove all pyc pyo files'
	@echo 'make tags       build ctags file'

ubuntu:
	sudo apt update
	sudo apt-get -y build-dep python-lxml python-psycopg2
	sudo apt-get -y install curl build-essential python-dev libxml2-dev libxslt1-dev zlib1g-dev libpng12-dev libjpeg-dev exuberant-ctags

bin/django: buildout.cfg bin/buildout config/versions.cfg config/base.cfg config/assets.cfg setup.py
	bin/buildout
	touch -c $@

buildout.cfg:
	echo '[buildout]' >> buildout.cfg
	echo 'extends = config/env/development.cfg' >> buildout.cfg

var/db.sqlite3:
	bin/django migrate

bin/flake8: bin/buildout

bin/pylint: bin/buildout

bin/buildout: bin/python
	bin/python bootstrap.py --version=2.2.1

bin/python: parts/virtualenv-$(VENV_VERSION)
	parts/virtualenv-$(VENV_VERSION)/virtualenv.py --python=python3 --no-site-packages .

parts/virtualenv-$(VENV_VERSION): parts
	wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-$(VENV_VERSION).tar.gz -O- | tar -xzf- -C parts
	touch -c $@

parts:
	mkdir -p parts

clean:
	rm -rf akl.lt.egg-info bin develop-eggs include .installed.cfg lib \
		   local parts share \
		   var eggs
	find akllt -type f -iname '*.egg-info' -delete
	find akllt -type f -iname '*.py[co]' -delete

cleanpyc:
	find akllt -type f -iname '*.py[co]' -delete

run: bin/django
	bin/django runserver 0.0.0.0:8000

testall: test flake8 pylint cleanpyc

test: bin/django
	bin/coverage erase
	bin/coverage run --source=akllt bin/django test --settings=akllt.settings.testing --nologcapture
	bin/coverage report --show-missing --fail-under=80

flake8: bin/flake8
	bin/flake8 --exclude=migrations akllt

pylint: bin/pylint
	bin/pylint --load-plugins pylint_django akllt

report:
	bin/coverage report --show-missing

tags: bin/django
	bin/ctags -v --tag-relative

.PHONY: all help clean cleanpyc run tags pylint test testall ubuntu
