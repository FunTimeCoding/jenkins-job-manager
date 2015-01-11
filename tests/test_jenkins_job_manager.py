from lib.jenkins_job_manager import JenkinsJobManager
from lxml import etree


def test_return_code():
    jjm = JenkinsJobManager()
    assert jjm.run() == 0

def test_bare_job():
    jjm = JenkinsJobManager()
    output = jjm.create_xml('https://github.com/FunTimeCoding/dotfiles.git', repo_type=None)

    my_parser = etree.XMLParser(remove_blank_text=True)
    original = etree.parse('tests/fixture/bare-job.xml', parser=my_parser)
    original_serialized = etree.tostring(original, encoding='unicode', pretty_print=True)

    assert original_serialized == output

def test_git_job():
    jjm = JenkinsJobManager()
    output = jjm.create_xml('https://github.com/FunTimeCoding/dotfiles.git')

    my_parser = etree.XMLParser(remove_blank_text=True)
    original = etree.parse('tests/fixture/git-job.xml', parser=my_parser)
    original_serialized = etree.tostring(original, encoding='unicode', pretty_print=True)

    assert original_serialized == output
