# JenkinsJobManager

## Setup

This section explains how to install and uninstall the project.

Install the project.

```sh
pip3 install git+https://git@github.com/FunTimeCoding/jenkins-job-manager.git#egg=jenkins-job-manager
pip3 install -i https://testpypi.python.org/pypi jenkins-job-manager
```

Uninstall the project.

```sh
pip3 uninstall jenkins-job-manager
```


## Usage

This section explains how to use the project.

Run the program.

```sh
jjm
```


## Development

This section explains how to improve the project.

Build the project. This installs dependencies.

```sh
./build.sh
```

Run tests, style check and spell check.

```sh
./spell-check.sh
./style-check.sh
./tests.sh
```

Build the package.

```sh
./package.sh
```

Install the experimental Debian package.

```sh
sudo dpkg --install build/python3-jenkins-job-manager_0.1.0-1_all.deb
```

Show files the package installed.

```sh
dpkg-query --listfiles python3-jenkins-job-manager
```
