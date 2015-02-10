# Python Skeleton


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
pip3 install nose2
```

Run tests.

```sh
nose2
```

Run ant like Jenkins. Requires `ant` to be installed.

```sh
ant
```


## Important details

* The reason why the `tests` directory is not called `test` is because of the nose2 convention.
