# JenkinsJobManager

## Setup

This section explains how to install and uninstall the project.

Install project dependencies.

```sh
script/setup.sh
```

Install pip package from GitHub.

```sh
pip3 install git+https://git@github.com/FunTimeCoding/jenkins-job-manager.git#egg=jenkins-job-manager
```

Install pip package from DevPi.

```sh
pip3 install -i https://testpypi.python.org/pypi jenkins-job-manager
```

Uninstall package.

```sh
pip3 uninstall jenkins-job-manager
```


## Usage

This section explains how to use the project.

Run the main program.

```sh
jjm
```


## Development

This section explains how to improve the project.

Configure Git on Windows before cloning. This avoids problems with Vagrant and VirtualBox.

```sh
git config --global core.autocrlf input
```

Create the development virtual machine on Linux and Darwin.

```sh
script/vagrant/create.sh
```

Create the development virtual machine on Windows.

```bat
script\vagrant\create.bat
```

Run tests, style check and metrics.

```sh
script/test.sh [--help]
script/check.sh [--help]
script/measure.sh [--help]
```

Build project.

```sh
script/build.sh
```

Install Debian package.

```sh
sudo dpkg --install build/python3-jenkins-job-manager_0.1.0-1_all.deb
```

Show files the package installed.

```sh
dpkg-query --listfiles python3-jenkins-job-manager
```
