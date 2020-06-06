from lxml.etree import Element

from jenkins_job_manager.freestyle_project_builder.publisher_settings import \
    PublisherSettings
from jenkins_job_manager.freestyle_project_builder \
    .publishers_generator import PublishersGenerator
from jenkins_job_manager.freestyle_project_builder.triggers_generator import \
    TriggersGenerator
from jenkins_job_manager.general_markup_generator import GeneralMarkupGenerator
from jenkins_job_manager.helper import Helper
from jenkins_job_manager.project_builder import ProjectBuilder
from jenkins_job_manager.repository_settings import RepositorySettings


class FreestyleProjectBuilder(ProjectBuilder):
    @property
    def labels(self) -> str:
        return self._labels

    @labels.getter
    def labels(self) -> str:
        return self._labels

    @labels.setter
    def labels(self, value: str) -> None:
        self._labels = value

    @property
    def build_command(self) -> str:
        return self._build_command

    @build_command.getter
    def build_command(self) -> str:
        return self._build_command

    @build_command.setter
    def build_command(self, value: str) -> None:
        self._build_command = value

    @property
    def publisher_settings(self) -> PublisherSettings:
        return self._publisher_settings

    @publisher_settings.getter
    def publisher_settings(self) -> PublisherSettings:
        return self._publisher_settings

    @publisher_settings.setter
    def publisher_settings(self, value: PublisherSettings) -> None:
        self._publisher_settings = value

    def __init__(
            self,
            repository_settings: RepositorySettings,
            publisher_settings: PublisherSettings
    ):
        super().__init__()
        self.labels = ''
        self.build_command = ''
        self.repository_settings = repository_settings
        self.publisher_settings = publisher_settings

    @staticmethod
    def _append_node_labels(element: Element, labels: str):
        if labels == '':
            element.append(
                Helper.create_true_boolean_element(tag='canRoam')
            )
        else:
            element.append(
                Helper.create_element_with_text(
                    tag='assignedNode',
                    text=labels,
                )
            )
            element.append(
                Helper.create_false_boolean_element(tag='canRoam')
            )

    def _append_general_markup(self, element: Element) -> None:
        generator = GeneralMarkupGenerator()
        element.append(
            Helper.create_false_boolean_element(tag='keepDependencies')
        )
        element.append(Element('properties'))
        element.append(
            generator.generate_scm_for_repository_type(
                locator=self.repository_settings.repository_locator,
                repository_type=self.repository_settings.repository_type
            )
        )
        FreestyleProjectBuilder._append_node_labels(
            element=element,
            labels=self.labels,
        )
        element.append(Helper.create_false_boolean_element(tag='disabled'))
        element.append(
            Helper.create_false_boolean_element(
                tag='blockBuildWhenDownstreamBuilding',
            )
        )
        element.append(
            Helper.create_false_boolean_element(
                tag='blockBuildWhenUpstreamBuilding',
            )
        )

    def _append_publishers(self, parent: Element) -> None:
        publishers = Element('publishers')
        PublishersGenerator.append_junit_publisher(
            parent=publishers,
            junit=self.publisher_settings.junit,
        )
        PublishersGenerator.append_checkstyle_publisher(
            parent=publishers,
            checkstyle=self.publisher_settings.checkstyle,
        )
        PublishersGenerator.append_jacoco_publisher(
            parent=publishers,
            jacoco=self.publisher_settings.jacoco,
        )
        PublishersGenerator.append_hypertext_report(
            parent=publishers,
            hypertext_report=self.publisher_settings.hypertext_report,
        )
        PublishersGenerator.append_recipients(
            parent=publishers,
            recipients=self.publisher_settings.recipients,
        )
        parent.append(publishers)

    @staticmethod
    def _append_builders(element: Element, build_command: str) -> None:
        builders = Element('builders')

        if build_command:
            shell = Element('hudson.tasks.Shell')
            shell.append(
                Helper.create_element_with_text(
                    tag='command',
                    text=build_command,
                )
            )
            builders.append(shell)

        element.append(builders)

    def build(self) -> Element:
        project = Element('project')
        project.append(Element('actions'))
        project.append(
            Helper.create_element_with_text(
                tag='description',
                text=self.description,
            )
        )
        self._append_general_markup(element=project)
        project.append(
            TriggersGenerator.generate(build_command=self.build_command)
        )
        project.append(
            Helper.create_false_boolean_element(tag='concurrentBuild')
        )
        FreestyleProjectBuilder._append_builders(
            element=project,
            build_command=self.build_command
        )
        self._append_publishers(parent=project)
        project.append(Element('buildWrappers'))

        return project
