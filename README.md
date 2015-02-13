# Jenkins Job Manager


## Setup

Install jenkins-job-manager.

```sh
pip3 install -e jenkins-job-manager
```

Uninstall jenkins-job-manager.

```sh
pip3 uninstall jenkins-job-manager
```


## Operation

Run the main script.

```sh
PYTHONPATH=. bin/jjm
```

```sh
jjm --url http://gitlab.ping.lan/shiin/jenkins-job-manager.git
```


## Development

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


## Important details

* The reason why the `tests` directory is not called `test` is because a package named `test` exists.
