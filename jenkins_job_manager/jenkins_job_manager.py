from sys import argv as argument_vector, exit as system_exit

from lxml.etree import Element

from jenkins_job_manager.custom_argument_parser import CustomArgumentParser
from jenkins_job_manager.freestyle_project_builder.freestyle_project_builder \
    import FreestyleProjectBuilder
from jenkins_job_manager.lxml_helper import serialize_element
from jenkins_job_manager.version_control_constants import \
    VersionControlConstants
from jenkins_job_manager.workflow_project_builder.workflow_project_builder \
    import WorkflowProjectBuilder


class JenkinsJobManager:
    FREESTYLE_JOB_TYPE = 'freestyle'
    WORKFLOW_JOB_TYPE = 'workflow'

    def __init__(self, arguments: list):
        parsed_arguments = self.create_parser().parse_args(arguments)
        self.repository_type = parsed_arguments.type
        self.repository_locator = parsed_arguments.locator
        self.build_command = parsed_arguments.build_command
        self.description = parsed_arguments.description
        self.junit = parsed_arguments.junit
        self.hypertext_report = parsed_arguments.hypertext_report
        self.checkstyle = parsed_arguments.checkstyle
        self.jacoco = parsed_arguments.jacoco
        self.recipients = parsed_arguments.recipients
        self.labels = parsed_arguments.labels
        self.job_type = parsed_arguments.job_type

        if self.is_valid_repository_type(self.repository_type) is False:
            self.repository_type = self.guess_repository_type(
                self.repository_locator
            )

    @staticmethod
    def main():
        system_exit(JenkinsJobManager(argument_vector[1:]).run())

    def run(self) -> int:
        print("<?xml version='1.1' encoding='UTF-8'?>")
        print(self.generate_serialized_xml().strip())

        return 0

    @staticmethod
    def get_repository_types() -> list:
        return [
            VersionControlConstants.GIT_TYPE,
            VersionControlConstants.SUBVERSION_TYPE
        ]

    @staticmethod
    def get_valid_job_types() -> list:
        return [
            JenkinsJobManager.FREESTYLE_JOB_TYPE,
            JenkinsJobManager.WORKFLOW_JOB_TYPE
        ]

    @staticmethod
    def is_valid_repository_type(repository_type: str) -> bool:
        return repository_type in JenkinsJobManager.get_repository_types()

    @staticmethod
    def guess_repository_type(locator: str) -> str:
        repository_type = ''

        for valid_type in JenkinsJobManager.get_repository_types():
            if valid_type in locator:
                repository_type = valid_type

                break

        return repository_type

    @staticmethod
    def create_parser() -> CustomArgumentParser:
        parser = CustomArgumentParser(
            description='Generate a configuration for a Jenkins job.'
        )

        required_group = parser.add_argument_group('required named arguments')
        required_group.add_argument(
            '--locator',
            help='locator to the repository to check out on Jenkins',
            required=True,
        )

        parser.add_argument(
            '--type',
            help='Repository type.',
            choices=JenkinsJobManager.get_repository_types(),
        )
        parser.add_argument(
            '--build-command',
            help='Set the build command.',
            default='',
        )
        parser.add_argument(
            '--junit',
            help='Set the JUnit output to publish.',
            default='',
        )
        parser.add_argument(
            '--hypertext-report',
            help='Set the hypertext report to publish.',
            default='',
        )
        parser.add_argument(
            '--checkstyle',
            help='Set the checkstyle output to publish.',
            default='',
        )
        parser.add_argument(
            '--jacoco',
            help='Enable publishing JaCoCo output.',
            action='store_true'
        )
        parser.add_argument(
            '--description',
            help='Set the job description.',
            default='',
        )
        parser.add_argument(
            '--labels',
            help='Set the job labels.',
            default='',
        )
        parser.add_argument(
            '--recipients',
            help='Set mail recipients in case of build failure, '
                 'whitespace-separated.',
            default='',
        )
        parser.add_argument(
            '--job-type',
            help='Job type.',
            choices=JenkinsJobManager.get_valid_job_types(),
            default=JenkinsJobManager.FREESTYLE_JOB_TYPE,
        )

        return parser

    def generate_xml(self) -> Element:
        if self.job_type is JenkinsJobManager.FREESTYLE_JOB_TYPE:
            freestyle_builder = FreestyleProjectBuilder()
            freestyle_builder.repository_locator = self.repository_locator
            freestyle_builder.description = self.description
            freestyle_builder.repository_type = self.repository_type
            freestyle_builder.labels = self.labels
            freestyle_builder.build_command = self.build_command
            freestyle_builder.junit = self.junit
            freestyle_builder.checkstyle = self.checkstyle
            freestyle_builder.hypertext_report = self.hypertext_report
            freestyle_builder.recipients = self.recipients
            freestyle_builder.jacoco = self.jacoco

            return freestyle_builder.build()
        elif self.job_type is JenkinsJobManager.WORKFLOW_JOB_TYPE:
            workflow_builder = WorkflowProjectBuilder()
            workflow_builder.repository_locator = self.repository_locator
            workflow_builder.description = self.description

            return workflow_builder.build()
        else:
            raise RuntimeError('Unexpected job type: ' + self.repository_type)

    def generate_serialized_xml(self) -> str:
        xml = self.generate_xml()

        return serialize_element(xml)
