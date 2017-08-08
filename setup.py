#!/usr/bin/env python3
from setuptools import setup

setup(
    name='jenkins-job-manager',
    version='0.1.0',
    description='Generate job configuration files for Jenkins.',
    url='https://github.com/FunTimeCoding/jenkins-job-manager',
    author='Alexander Reitzel',
    author_email='funtimecoding@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['lxml'],
    scripts=['bin/jjm'],
    packages=['jenkins_job_manager'],
    download_url='http://funtimecoding.org/jenkins-job-manager.tar.gz',
)
