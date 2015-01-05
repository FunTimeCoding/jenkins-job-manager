from lib.jenkins_job_manager import JenkinsJobManager


def tests_can_be_functions():
    jjm = JenkinsJobManager()
    assert jjm.run() == 0
