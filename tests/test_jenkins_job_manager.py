from jenkins_job_manager.jenkins_job_manager import JenkinsJobManager
from lxml import etree
from lxml.etree import Element, XMLParser
from tests.helper.xml_comparator import xml_compare
from tests.helper.string_type_detector import get_string_type

GIT_FIXTURE_URL = 'http://example.org/my_git_repo.git'
SVN_FIXTURE_URL = 'http://example.org/my_svn_repo'


def test_plain_run_returns_zero():
    jjm = JenkinsJobManager([])
    assert jjm.run() == 0


def test_create_xml_without_repo():
    jjm = JenkinsJobManager([])
    my_parser = XMLParser(remove_blank_text=True)

    fixture_tree = etree.parse('tests/fixture/bare-job.xml', parser=my_parser)
    fixture_root_node = fixture_tree.getroot()
    serialized_xml_fixture = etree.tostring(fixture_root_node,
                                            encoding='unicode',
                                            pretty_print=True)

    serialized_xml_generated = jjm.create_xml()
    generated_root_node = serialized_to_element(serialized_xml_generated)

    print('serialized_xml_fixture: ' + serialized_xml_fixture)
    print('serialized_xml_generated: ' + serialized_xml_generated)
    # assert type(fixture_root_node) == Element
    # assert type(generated_root_node) == Element
    assert xml_compare(fixture_root_node, generated_root_node) == True
    assert serialized_xml_fixture == serialized_xml_generated


def test_create_xml_with_git_repo():
    jjm = JenkinsJobManager(['--url', GIT_FIXTURE_URL])
    my_parser = XMLParser(remove_blank_text=True)

    fixture_tree = etree.parse('tests/fixture/git-job.xml', parser=my_parser)
    fixture_root_node = fixture_tree.getroot()
    clear_properties_node(fixture_root_node)
    serialized_xml_fixture = etree.tostring(fixture_root_node,
                                            encoding='unicode',
                                            pretty_print=True)

    serialized_xml_generated = jjm.create_xml(GIT_FIXTURE_URL,
                                              repo_type='git')
    generated_root_node = serialized_to_element(serialized_xml_generated)

    print('serialized_xml_fixture: ' + serialized_xml_fixture)
    print('serialized_xml_generated: ' + serialized_xml_generated)
    # assert type(fixture_root_node) == Element
    # assert type(generated_root_node) == Element
    assert xml_compare(fixture_root_node, generated_root_node) == True
    assert serialized_xml_fixture == serialized_xml_generated


def test_create_xml_with_svn_repo():
    jjm = JenkinsJobManager(['--url', SVN_FIXTURE_URL])
    my_parser = XMLParser(remove_blank_text=True)

    fixture_tree = etree.parse('tests/fixture/svn-job.xml', parser=my_parser)
    fixture_root_node = fixture_tree.getroot()
    clear_properties_node(fixture_root_node)
    serialized_xml_fixture = etree.tostring(fixture_root_node,
                                            encoding='unicode',
                                            pretty_print=True)

    serialized_xml_generated = jjm.create_xml(SVN_FIXTURE_URL,
                                              repo_type='svn')
    generated_root_node = serialized_to_element(serialized_xml_generated)

    print('serialized_xml_fixture: ' + serialized_xml_fixture)
    print('serialized_xml_generated: ' + serialized_xml_generated)
    # assert type(fixture_root_node) == Element
    # assert type(generated_root_node) == Element
    assert xml_compare(fixture_root_node, generated_root_node) == True
    assert serialized_xml_fixture == serialized_xml_generated


def clear_properties_node(xml):
    properties = xml.find('properties')
    for node in properties.findall('*'):
        properties.remove(node)


def test_correct_return_types():
    jjm = JenkinsJobManager([])
    my_parser = XMLParser(remove_blank_text=True)

    fixture_tree = etree.parse('tests/fixture/bare-job.xml', parser=my_parser)
    fixture_root_node = fixture_tree.getroot()
    serialized_xml_fixture = etree.tostring(fixture_root_node,
                                            encoding='unicode',
                                            pretty_print=True)

    serialized_xml_generated = jjm.create_xml(SVN_FIXTURE_URL)
    generated_root_node = serialized_to_element(serialized_xml_generated)

    # assert type(fixture_root_node) == Element
    # assert type(generated_root_node) == Element
    assert get_string_type(serialized_xml_fixture) == 'str'
    assert get_string_type(serialized_xml_generated) == 'str'
    assert type(serialized_xml_fixture) == str
    assert type(serialized_xml_generated) == str


def test_repo_type():
    git_url_type = JenkinsJobManager.guess_repo_type(GIT_FIXTURE_URL)
    assert git_url_type == 'git'

    svn_url_type = JenkinsJobManager.guess_repo_type(SVN_FIXTURE_URL)
    assert svn_url_type == 'svn'

    no_url_type = JenkinsJobManager.guess_repo_type('')
    assert no_url_type == ''


def test_repo_types():
    for repo_type in JenkinsJobManager.get_valid_repo_types():
        assert type(repo_type) == str


def serialized_to_element(serialized: str) -> Element:
    parser = XMLParser(remove_blank_text=True)
    element = etree.fromstring(serialized, parser=parser)

    return element
