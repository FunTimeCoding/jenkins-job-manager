from jenkins_job_manager.jenkins_job_manager import JenkinsJobManager
from lxml import etree
from lxml.etree import Element, XMLParser
from jenkins_job_manager.lxml_helper import serialize_element
from tests.helper.xml_comparator import xml_compare

GIT_FIXTURE_URL = 'http://example.org/my_git_repo.git'
GITHUB_FIXTURE_URL = 'http://github.com/username/my_git_repo'
UNKNOWN_FIXTURE_URL = 'http://example.org/no_known_repo_type'
SVN_FIXTURE_URL = 'http://example.org/my_svn_repo'


def test_plain_run_returns_zero():
    jjm = JenkinsJobManager([])
    assert jjm.run() == 0


def test_create_xml_without_repo():
    fixture = load_fixture('tests/fixture/bare-job.xml')
    fixture_serialized = serialize_element(fixture)

    jjm = JenkinsJobManager([])
    generated = jjm.generate_xml()
    generated_serialized = jjm.generate_serialized_xml()

    print('fixture_serialized: ' + fixture_serialized)
    print('generated_serialized: ' + generated_serialized)

    assert xml_compare(fixture, generated) == True
    assert fixture_serialized == generated_serialized


def test_create_xml_with_git_repo():
    fixture = load_fixture('tests/fixture/git-job.xml')
    fixture_serialized = serialize_element(fixture)

    jjm = JenkinsJobManager(['--url', GIT_FIXTURE_URL])
    generated = jjm.generate_xml()
    generated_serialized = jjm.generate_serialized_xml()

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
    assert JenkinsJobManager.guess_repo_type(GIT_FIXTURE_URL) == 'git'
    assert JenkinsJobManager.guess_repo_type(SVN_FIXTURE_URL) == 'svn'
    assert JenkinsJobManager.guess_repo_type(GITHUB_FIXTURE_URL) == 'git'
    assert JenkinsJobManager.guess_repo_type(UNKNOWN_FIXTURE_URL) == ''


def test_create_xml_with_svn_repo():
    fixture = load_fixture('tests/fixture/svn-job.xml')
    fixture_serialized = serialize_element(fixture)

    jjm = JenkinsJobManager(['--url', SVN_FIXTURE_URL])
    generated = jjm.generate_xml()
    generated_serialized = jjm.generate_serialized_xml()

    print('fixture_serialized: ' + fixture_serialized)
    print('generated_serialized: ' + generated_serialized)

    assert xml_compare(fixture, generated) == True
    assert fixture_serialized == generated_serialized


def test_create_xml_build_command():
    fixture = load_fixture('tests/fixture/python-build-job.xml')
    fixture_serialized = serialize_element(fixture)

    jjm = JenkinsJobManager(['--url', GIT_FIXTURE_URL, '--build'])
    generated_serialized = jjm.generate_serialized_xml()
    generated = jjm.generate_xml()

    print('fixture_serialized: ' + fixture_serialized)
    print('generated_serialized: ' + generated_serialized)

    assert xml_compare(fixture, generated) == True
    assert fixture_serialized == generated_serialized


def clear_properties_node(xml):
    properties = xml.find('properties')
    for node in properties.findall('*'):
        properties.remove(node)


def test_return_types():
    fixture = load_fixture('tests/fixture/bare-job.xml')
    jjm = JenkinsJobManager([])

    assert type(fixture).__name__ == '_Element'
    assert type(jjm.generate_xml()).__name__ == '_Element'
    assert type(serialize_element(fixture)) == str
    assert type(jjm.generate_serialized_xml()) == str


def test_repo_type():
    assert JenkinsJobManager.guess_repo_type(GIT_FIXTURE_URL) == 'git'
    assert JenkinsJobManager.guess_repo_type(SVN_FIXTURE_URL) == 'svn'
    assert JenkinsJobManager.guess_repo_type('') == ''


def test_repo_types():
    for repo_type in JenkinsJobManager.get_valid_repo_types():
        assert type(repo_type) == str
