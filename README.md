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


## Testing

Install test tools.

```sh
pip3 install -U pytest pytest-cov
```

Run tests.

```sh
./run-tests.sh
```

Run `ant` like Jenkins. Requires `ant` to be installed.

```sh
ant
```


## Important details

* The reason why the `tests` directory is not called `test` is because of the nose2 convention.
