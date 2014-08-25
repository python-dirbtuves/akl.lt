bin/django: bin/node bin/buildout buildout.cfg versions.cfg
	find src -type f -iname '*.pyc' -exec rm {} +
	bin/buildout

bin/buildout: bin/python
	bin/python bootstrap.py --version=2.2.1

bin/python: parts/virtualenv-1.11.6
	parts/virtualenv-1.11.6/virtualenv.py --python=python2.7 --setuptools --no-site-packages .

bin/node: bin/nodeenv
	bin/nodeenv --node=0.11.13 --prebuilt -p --requirements=node-requirements.txt
	touch -c $@

bin/nodeenv: bin/python requirements.txt
	bin/pip install -r requirements.txt

parts/virtualenv-1.11.6:
	mkdir -p parts
	wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.6.tar.gz -O- | tar -xzf- -C parts

clean:
	rm -rf akl.lt.egg-info bin develop-eggs include .installed.cfg lib \
		   local parts share $(wildcard src/node-v0.*.*-*-*/) \
		   $(wildcard src/*.egg-info/) var eggs

run:
	bin/django runserver --settings=akllt.settings.development

.PHONY: clean run
