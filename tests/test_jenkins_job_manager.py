from lxml import etree
from lxml.etree import Element, XMLParser

from jenkins_job_manager.jenkins_job_manager import JenkinsJobManager
from jenkins_job_manager.lxml_helper import serialize_element
from tests.helper.xml_comparator import xml_compare

GIT_FIXTURE_LOCATOR = 'http://example.org/my_git_repo.git'
GITHUB_FIXTURE_LOCATOR = 'http://github.com/username/my_git_repo'
UNKNOWN_FIXTURE_LOCATOR = 'http://example.org/no_known_repo_type'
SVN_FIXTURE_LOCATOR = 'http://example.org/my_svn_repo'


def test_no_locator():
    try:
        JenkinsJobManager([])
        assert False
    except SystemExit as exception:
        assert str(exception) == '1'


def test_create_xml_with_git_repo():
    fixture = load_fixture('tests/fixture/git-job.xml')
    fixture_serialized = serialize_element(fixture)

    application = JenkinsJobManager(['--locator', GIT_FIXTURE_LOCATOR])
    generated = application.generate_xml()
    generated_serialized = application.generate_serialized_xml()

    print('fixture_serialized: ' + fixture_serialized)
    print('generated_serialized: ' + generated_serialized)

    assert xml_compare(fixture, generated) == True
    assert fixture_serialized == generated_serialized


def load_fixture(path: str) -> Element:
    my_parser = XMLParser(remove_blank_text=True)
    fixture_tree = etree.parse(path, parser=my_parser)
    fixture_root_node = fixture_tree.getroot()
    clear_properties_node(fixture_root_node)

    return fixture_root_node


def test_repo_type():
    assert JenkinsJobManager.guess_repo_type(GIT_FIXTURE_LOCATOR) == 'git'
    assert JenkinsJobManager.guess_repo_type(SVN_FIXTURE_LOCATOR) == 'svn'
    assert JenkinsJobManager.guess_repo_type(GITHUB_FIXTURE_LOCATOR) == 'git'
    assert JenkinsJobManager.guess_repo_type(UNKNOWN_FIXTURE_LOCATOR) == ''


def test_create_xml_with_svn_repo():
    fixture = load_fixture('tests/fixture/svn-job.xml')
    fixture_serialized = serialize_element(fixture)

    application = JenkinsJobManager(['--locator', SVN_FIXTURE_LOCATOR])
    generated = application.generate_xml()
    generated_serialized = application.generate_serialized_xml()

    print('fixture_serialized: ' + fixture_serialized)
    print('generated_serialized: ' + generated_serialized)

    assert xml_compare(fixture, generated) == True
    assert fixture_serialized == generated_serialized


def test_create_xml_build_command():
    fixture = load_fixture('tests/fixture/python-build-job.xml')
    fixture_serialized = serialize_element(fixture)

    application = JenkinsJobManager(
        ['--locator', GIT_FIXTURE_LOCATOR, '--build']
    )
    generated_serialized = application.generate_serialized_xml()
    generated = application.generate_xml()

    print('fixture_serialized: ' + fixture_serialized)
    print('generated_serialized: ' + generated_serialized)

    assert xml_compare(fixture, generated) == True
    assert fixture_serialized == generated_serialized


def clear_properties_node(xml):
    properties = xml.find('properties')
    for node in properties.findall('*'):
        properties.remove(node)


def test_return_types():
    fixture = load_fixture('tests/fixture/git-job.xml')
    application = JenkinsJobManager(['--locator', GIT_FIXTURE_LOCATOR])

    assert type(fixture).__name__ == '_Element'
    assert type(application.generate_xml()).__name__ == '_Element'
    assert isinstance(serialize_element(fixture), str) == True
    assert isinstance(application.generate_serialized_xml(), str) == True


def test_guess_repo_type():
    for repo_type in JenkinsJobManager.get_valid_repo_types():
        assert isinstance(repo_type, str) == True

    assert JenkinsJobManager.guess_repo_type(GIT_FIXTURE_LOCATOR) == 'git'
    assert JenkinsJobManager.guess_repo_type(SVN_FIXTURE_LOCATOR) == 'svn'
    assert JenkinsJobManager.guess_repo_type('') == ''
