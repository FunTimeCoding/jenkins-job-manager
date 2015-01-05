try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Stub description for example-project.',
    'author': 'Alexander Reitzel',
    'url': 'http://funtimecoding.org',
    'download_url': 'http://funtimecoding.org/download/example-project.tar.gz',
    'author_email': 'funtimecoding@gmail.com',
    'version': '0.1',
    'install_requires': ['nose2'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'example-project'
}

setup(**config)
