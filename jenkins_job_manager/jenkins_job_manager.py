from argparse import Namespace
from sys import argv as argument_vector, exit as system_exit

from lxml.etree import Element
from python_utility.custom_argument_parser import CustomArgumentParser

from jenkins_job_manager.freestyle_project_builder.freestyle_settings \
    import FreestyleSettings
from jenkins_job_manager.freestyle_project_builder.freestyle_project_builder \
    import FreestyleProjectBuilder
from jenkins_job_manager.freestyle_project_builder.publisher_settings \
    import PublisherSettings
from jenkins_job_manager.lxml_helper import serialize_element
from jenkins_job_manager.project_builder import ProjectBuilder
from jenkins_job_manager.repository_settings import RepositorySettings
from jenkins_job_manager.workflow_project_builder.workflow_project_builder \
    import WorkflowProjectBuilder


class JenkinsJobManager:
    FREESTYLE_JOB_TYPE = 'freestyle'
    WORKFLOW_JOB_TYPE = 'workflow'

    def __init__(self, arguments: list):
        self.parsed_arguments = self._create_parser().parse_args(arguments)

    @staticmethod
    def create_publisher_settings(
            parsed_arguments: Namespace
    ) -> PublisherSettings:
        publisher_settings = PublisherSettings()
        publisher_settings.junit = parsed_arguments.junit
        publisher_settings.hypertext_report = parsed_arguments.hypertext_report
        publisher_settings.checkstyle = parsed_arguments.checkstyle
        publisher_settings.jacoco = parsed_arguments.jacoco
        publisher_settings.recipients = parsed_arguments.recipients

        return publisher_settings

    @staticmethod
    def main():
        system_exit(JenkinsJobManager(argument_vector[1:]).run())

    def run(self) -> int:
        print('<?xml version="1.1" encoding="UTF-8"?>')
        print(self.generate_serialized_xml().strip())

        return 0

    @staticmethod
    def get_job_types() -> list:
        return [
            JenkinsJobManager.FREESTYLE_JOB_TYPE,
            JenkinsJobManager.WORKFLOW_JOB_TYPE
        ]

    @staticmethod
    def _add_required_arguments(parser: CustomArgumentParser) -> None:
        required_group = parser.add_argument_group('required named arguments')
        required_group.add_argument(
            '--locator',
            help='locator to the repository to check out on Jenkins',
            required=True,
        )

    @staticmethod
    def _add_publisher_arguments(parser: CustomArgumentParser) -> None:
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
            action='store_true',
        )

    @staticmethod
    def _create_parser() -> CustomArgumentParser:
        parser = CustomArgumentParser(
            description='Generate a configuration for a Jenkins job.'
        )
        JenkinsJobManager._add_required_arguments(parser=parser)
        parser.add_argument(
            '--type',
            help='Repository type.',
            choices=RepositorySettings.get_repository_types(),
        )
        parser.add_argument(
            '--build-command',
            help='Set the build command.',
            default='',
        )
        JenkinsJobManager._add_publisher_arguments(parser=parser)
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
            choices=JenkinsJobManager.get_job_types(),
            default=JenkinsJobManager.FREESTYLE_JOB_TYPE,
        )

        return parser

    def generate_xml(self) -> Element:
        builder: ProjectBuilder
        repository_settings = RepositorySettings(
            repository_type=self.parsed_arguments.type,
            repository_locator=self.parsed_arguments.locator,
        )

        if self.parsed_arguments.job_type is JenkinsJobManager \
                .FREESTYLE_JOB_TYPE:
            builder = FreestyleProjectBuilder(
                repository_settings=repository_settings,
                publisher_settings=JenkinsJobManager.create_publisher_settings(
                    parsed_arguments=self.parsed_arguments
                ),
                freestyle_settings=FreestyleSettings(
                    build_command=self.parsed_arguments.build_command,
                    labels=self.parsed_arguments.labels,
                ),
            )
        elif self.parsed_arguments.job_type is JenkinsJobManager \
                .WORKFLOW_JOB_TYPE:
            builder = WorkflowProjectBuilder(
                repository_settings=repository_settings,
            )
        else:
            raise RuntimeError(
                'Unexpected job type: ' + self.parsed_arguments.job_type
            )

        builder.description = self.parsed_arguments.description

        return builder.build()

    def generate_serialized_xml(self) -> str:
        return serialize_element(self.generate_xml())
