from jenkins_job_manager.jenkins_job_manager import JenkinsJobManager
from jenkins_job_manager.lxml_helper import serialize_element
from tests.helper import load_fixture

GIT_LOCATOR = 'http://example.org/my_git_repo.git'
GITHUB_LOCATOR = 'http://github.com/username/my_git_repo'
UNKNOWN_LOCATOR = 'http://example.org/no_known_repository_type'
SUBVERSION_LOCATOR = 'http://example.org/my_svn_repo'


def test_missing_locator() -> None:
    try:
        JenkinsJobManager([])
        assert False
    except SystemExit as exception:
        assert str(exception) == '1'


def test_generate_with_git_repository() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/git-repository.xml')
    )
    application = JenkinsJobManager(['--locator', GIT_LOCATOR])
    assert fixture == application.generate_serialized_xml()


def test_guess_repository_type() -> None:
    assert JenkinsJobManager.guess_repository_type(GIT_LOCATOR) == 'git'
    assert JenkinsJobManager.guess_repository_type(SUBVERSION_LOCATOR) == 'svn'
    assert JenkinsJobManager.guess_repository_type(GITHUB_LOCATOR) == 'git'
    assert JenkinsJobManager.guess_repository_type(UNKNOWN_LOCATOR) == ''


def test_generate_with_subversion_repository() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/subversion-repository.xml')
    )
    application = JenkinsJobManager(['--locator', SUBVERSION_LOCATOR])
    assert fixture == application.generate_serialized_xml()


def test_generate_with_build_command() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/build-command.xml')
    )
    application = JenkinsJobManager(
        ['--locator', GIT_LOCATOR, '--build', './build.sh']
    )
    assert fixture == application.generate_serialized_xml()


def test_generate_with_multi_line_build_command() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/multi-line-build-command.xml')
    )
    command = 'export PATH="${HOME}/opt/python-3.5.1/bin:${PATH}"' \
              + "\n./build.sh"
    application = JenkinsJobManager(
        ['--locator', GIT_LOCATOR, '--build', command]
    )
    assert fixture == application.generate_serialized_xml()


def test_generate_with_description() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/description.xml')
    )
    application = JenkinsJobManager(
        ['--locator', GIT_LOCATOR, '--description', 'example']
    )
    assert fixture == application.generate_serialized_xml()


def test_generate_with_junit_publish() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/junit-publish.xml')
    )
    application = JenkinsJobManager(
        ['--locator', GIT_LOCATOR, '--junit', 'build/junit.xml']
    )
    assert fixture == application.generate_serialized_xml()


def test_generate_with_hypertext_report() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/hypertext-report.xml')
    )
    application = JenkinsJobManager(
        [
            '--locator', GIT_LOCATOR,
            '--hypertext-report', 'mess_detector'
        ]
    )
    assert fixture == application.generate_serialized_xml()


def test_generate_with_checkstyle_publish() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/checkstyle-publish.xml')
    )
    application = JenkinsJobManager(
        [
            '--locator', GIT_LOCATOR,
            '--checkstyle', 'build/log/checkstyle-*.xml'
        ]
    )
    assert fixture == application.generate_serialized_xml()


def test_generate_with_recipients() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/recipients.xml')
    )
    application = JenkinsJobManager(
        [
            '--locator', GIT_LOCATOR,
            '--recipients', 'example@example.org'
        ]
    )
    assert fixture == application.generate_serialized_xml()


def test_generate_with_labels() -> None:
    fixture = serialize_element(
        load_fixture('tests/fixture/labels.xml')
    )
    application = JenkinsJobManager(
        [
            '--locator', GIT_LOCATOR,
            '--labels', 'label1 && label2'
        ]
    )
    assert fixture == application.generate_serialized_xml()


def test_serialize_element_return_type() -> None:
    fixture = load_fixture('tests/fixture/git-repository.xml')
    assert isinstance(serialize_element(fixture), str) is True


def test_generate_xml_return_type() -> None:
    application = JenkinsJobManager(['--locator', GIT_LOCATOR])
    assert type(application.generate_xml()).__name__ == '_Element'


def test_generate_serialized_xml_return_type() -> None:
    application = JenkinsJobManager(['--locator', GIT_LOCATOR])
    assert isinstance(application.generate_serialized_xml(), str) is True


def test_valid_repository_types_are_strings() -> None:
    for repository_type in JenkinsJobManager.get_valid_repository_types():
        assert isinstance(repository_type, str) is True
