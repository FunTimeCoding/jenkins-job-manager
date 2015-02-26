"""Package metadata containing useful information."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

url = 'http://funtimecoding.org/download/jenkins-job-manager.tar.gz'
setup(name='jenkins-job-manager',
      description='Stub description for jenkins-job-manager.',
      author='Alexander Reitzel',
      url='http://funtimecoding.org',
      download_url=url,
      author_email='funtimecoding@gmail.com',
      version='0.1',
      install_requires=['lxml'],
      packages=[],
      scripts=['bin/jjm'])
