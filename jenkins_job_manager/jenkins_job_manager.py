from sys import argv as argument_vector, exit as system_exit

from lxml.etree import Element

from python_utility.custom_argument_parser import CustomArgumentParser
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
        parsed_arguments = self._create_parser().parse_args(arguments)
        self.repository_settings = RepositorySettings(
            repository_type=parsed_arguments.type,
            repository_locator=parsed_arguments.locator,
        )
        self.build_command = parsed_arguments.build_command
        self.description = parsed_arguments.description

        publisher_settings = PublisherSettings()
        publisher_settings.junit = parsed_arguments.junit
        publisher_settings.hypertext_report = parsed_arguments.hypertext_report
        publisher_settings.checkstyle = parsed_arguments.checkstyle
        publisher_settings.jacoco = parsed_arguments.jacoco
        publisher_settings.recipients = parsed_arguments.recipients
        self.publisher_settings = publisher_settings

        self.labels = parsed_arguments.labels
        self.job_type = parsed_arguments.job_type

    @staticmethod
    def main():
        system_exit(JenkinsJobManager(argument_vector[1:]).run())

    def run(self) -> int:
        print("<?xml version='1.1' encoding='UTF-8'?>")
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

    def _add_common_arguments(
            self,
            builder: ProjectBuilder
    ) -> None:
        builder.repository_settings = self.repository_settings
        builder.description = self.description

    def _add_parsed_publisher_arguments(
            self,
            freestyle_builder: FreestyleProjectBuilder
    ) -> None:
        freestyle_builder.publisher_settings = self.publisher_settings

    def _create_freestyle_builder(self) -> ProjectBuilder:
        freestyle_builder = FreestyleProjectBuilder(
            repository_settings=self.repository_settings,
            publisher_settings=self.publisher_settings,
        )
        self._add_common_arguments(builder=freestyle_builder)
        freestyle_builder.labels = self.labels
        self._add_parsed_publisher_arguments(
            freestyle_builder=freestyle_builder
        )
        freestyle_builder.build_command = self.build_command

        return freestyle_builder

    def _create_workflow_builder(self) -> ProjectBuilder:
        workflow_builder = WorkflowProjectBuilder(
            repository_settings=self.repository_settings,
        )
        self._add_common_arguments(builder=workflow_builder)

        return workflow_builder

    def generate_xml(self) -> Element:
        if self.job_type is JenkinsJobManager.FREESTYLE_JOB_TYPE:
            builder = self._create_freestyle_builder()
        elif self.job_type is JenkinsJobManager.WORKFLOW_JOB_TYPE:
            builder = self._create_workflow_builder()
        else:
            raise RuntimeError('Unexpected job type: ' + self.job_type)

        return builder.build()

    def generate_serialized_xml(self) -> str:
        return serialize_element(self.generate_xml())
