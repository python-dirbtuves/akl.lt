bin/django: bin/buildout buildout.cfg versions.cfg
	bin/buildout

bin/buildout: bin/python parts/index/django-1.7c2.tar.gz
	bin/python bootstrap.py --version=2.2.1

bin/django-admin.py: bin/python
	bin/pip install -r requirements.txt

parts/index/django-1.7c2.tar.gz:
	mkdir -p parts/index
	wget https://www.djangoproject.com/download/1.7c2/tarball/ -O parts/index/django-1.7c2.tar.gz

bin/python: parts/virtualenv-1.11.6
	parts/virtualenv-1.11.6/virtualenv.py --python=python2.7 --setuptools --no-site-packages .

parts/virtualenv-1.11.6:
	mkdir -p parts
	wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.6.tar.gz -O- | tar -xzf- -C parts

clean:
	rm -rf akl.lt.egg-info bin develop-eggs include .installed.cfg lib local parts

.PHONY: clean
