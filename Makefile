bin/django: var/assets/jquery/bower.json bin/buildout buildout.cfg versions.cfg setup.py
	find src -type f -iname '*.pyc' -exec rm {} +
	bin/buildout
	touch -c $@

bin/buildout: bin/python
	bin/python bootstrap.py --version=2.2.1

bin/python: parts/virtualenv-1.11.6
	parts/virtualenv-1.11.6/virtualenv.py --python=python2.7 --setuptools --no-site-packages .

var/assets/jquery/bower.json: bin/node bower.json
	if [ -n "$$NODE_VIRTUAL_ENV" -a "$$NODE_VIRTUAL_ENV" = "$$PWD" ] ; then \
	    bower install ; \
	else \
	    . bin/activate && bower install ; \
	fi
	touch -c $@

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

run: bin/django
	bin/django runserver --settings=akllt.settings.development

tags: bin/django
	bin/tags -v

.PHONY: clean run tags
