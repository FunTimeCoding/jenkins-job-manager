try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Stub description for jenkins-job-manager.',
    'author': 'Alexander Reitzel',
    'url': 'http://funtimecoding.org',
    'download_url': 'http://funtimecoding.org/download/jenkins-job-manager.tar.gz',
    'author_email': 'funtimecoding@gmail.com',
    'version': '0.1',
    'install_requires': ['nose2', 'lxml'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'jenkins-job-manager'
}

setup(**config)
