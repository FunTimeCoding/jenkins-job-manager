from lib.jenkins_job_manager import JenkinsJobManager


def test_return_code():
    jjm = JenkinsJobManager()
    assert jjm.run() == 0
