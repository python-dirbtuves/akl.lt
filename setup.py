from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='akl.lt',
    version='0.1.0',
    description='AKL web site',
    long_description=long_description,
    url='https://github.com/python-dirbtuves/akl.lt',
    author='Python dirbtuves',
    author_email='python-dirbtuves@googlegroups.com',
    license='AGPL',
    keywords='website',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'django',
        'coverage',
        # We have to specify webtest explicitly, because of this bug:
        # https://github.com/kmike/django-webtest/issues/28
        'webtest',
        'django-nose',
        'django-require',
        'django-compressor',
        'django-libsass',
        'django-webtest',
        'lxml',
        'wagtail',
        'tqdm',
        'django-extensions',
        'django-allauth',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
