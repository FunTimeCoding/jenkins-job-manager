from lib.jenkins_job_manager import JenkinsJobManager
from lxml import etree
from tests.helper.xml_comparator import xml_compare
from tests.helper.string_type_detector import get_string_type


def test_return_code():
    jjm = JenkinsJobManager()
    assert jjm.run() == 0


def test_bare_job():
    jjm = JenkinsJobManager()
    my_parser = etree.XMLParser(remove_blank_text=True)

    serialized_a = jjm.create_xml('https://github.com/FunTimeCoding/dotfiles.git', repo_type=None)
    root_a = etree.fromstring(serialized_a, parser=my_parser)

    tree_b = etree.parse('tests/fixture/bare-job.xml', parser=my_parser)
    root_b = tree_b.getroot()
    serialized_b = etree.tostring(root_b, encoding='unicode', pretty_print=True)

    print('root_a: ' + str(type(root_a)))
    print('root_b: ' + str(type(root_b)))
    assert xml_compare(root_a, root_b) == True

    print('serialized_a:' + str(type(serialized_a)))
    print('serialized_b:' + str(type(serialized_b)))
    assert type(serialized_a) == str
    assert type(serialized_b) == str

    print('serialized_a: ' + serialized_a)
    print('serialized_b: ' + serialized_b)
    assert serialized_a == serialized_b


def test_git_job():
    jjm = JenkinsJobManager()
    my_parser = etree.XMLParser(remove_blank_text=True)

    tree_a = etree.parse('tests/fixture/git-job.xml', parser=my_parser)
    root_a = tree_a.getroot()
    serialized_a = etree.tostring(root_a, encoding='unicode', pretty_print=True)

    serialized_b = jjm.create_xml('https://github.com/FunTimeCoding/dotfiles.git')
    root_b = etree.fromstring(serialized_b, parser=my_parser)

    print('root_a: ' + str(type(root_a)))
    print('root_b: ' + str(type(root_b)))
    assert xml_compare(root_a, root_b) == True

    print('serialized_a:' + str(type(serialized_a)))
    print('serialized_b:' + str(type(serialized_b)))
    assert type(serialized_a) == str
    assert type(serialized_b) == str

    print('serialized_a: ' + serialized_a)
    print('serialized_b: ' + serialized_b)
    assert serialized_a == serialized_b


def test_svn_job():
    assert False


def test_repo_type_git():
    jjm = JenkinsJobManager()
    assert jjm.guess_repo_type("https://github.com/FunTimeCoding/dotfiles.git") == "git"


def test_repo_type_svn():
    jjm = JenkinsJobManager()
    assert jjm.guess_repo_type("svn+ssh://svn.rz.adition/adition_v4/branches/release-v4.28") == "svn"


def test_is_str_not_bytes():
    my_parser = etree.XMLParser(remove_blank_text=True)

    # negative test
    tree_a = etree.parse('tests/fixture/git-job.xml', parser=my_parser)
    root_a = tree_a.getroot()
    serialized_a = etree.tostring(root_a, pretty_print=True)

    assert get_string_type(serialized_a) == "bytes"
    assert type(serialized_a) == bytes

    # this is how it's supposed to be
    tree_b = etree.parse('tests/fixture/git-job.xml', parser=my_parser)
    root_b = tree_b.getroot()
    serialized_b = etree.tostring(root_b, encoding='unicode', pretty_print=True)

    assert get_string_type(serialized_b) == "str"
    assert type(serialized_b) == str
