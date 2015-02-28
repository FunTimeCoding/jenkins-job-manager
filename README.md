# JenkinsJobManager


## Setup

Install the project from a local clone.

```sh
pip3 install -e ../jenkins-job-manager
```

Install the project from GitHub.

```sh
pip3 install git+git://github.com/FunTimeCoding/jenkins-job-manager.git
```

Uninstall the project.

```sh
pip3 uninstall jenkins-job-manager
```


## Development

Run the main script without having to install the project.

```sh
PYTHONPATH=. bin/jjm
```

Install development tools.

```sh
pip3 install -U pytest pytest-cov pylint pep8
```

Run code style check, lint check and tests.

```sh
./run-code-style-check.sh
./run-lint-check.sh
./run-tests.sh
```

Run `ant` like Jenkins. Requires `ant` to be installed. This generates reports in the `build` directory.

```sh
ant
```


## Skeleton details

* The reason why the `tests` directory is not called `test` is because a package named `test` exists.
* The main source code directory is the same name as the package in python packages.
* Dashes in project names become underscores in python code. They are still legit.
