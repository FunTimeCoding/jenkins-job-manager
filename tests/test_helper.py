from tests.helper import load_fixture


def test_load_fixture_return_type() -> None:
    fixture = load_fixture('tests/fixture/git-repository.xml')
    assert type(fixture).__name__ == '_Element'
