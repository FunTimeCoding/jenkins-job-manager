#!/usr/bin/env python3
from setuptools import setup

setup(
    name='jenkins-job-manager',
    version='0.1',
    description='Stub description for jenkins-job-manager.',
    install_requires=['lxml'],
    scripts=['bin/jjm'],
    packages=['jenkins_job_manager'],
    author='Alexander Reitzel',
    author_email='funtimecoding@gmail.com',
    url='http://example.org',
    download_url='http://example.org/jenkins-job-manager.tar.gz'
)
