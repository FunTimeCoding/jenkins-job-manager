from lxml.etree import Element

from jenkins_job_manager.freestyle_project_builder.mailer_generator import \
    MailerGenerator
from jenkins_job_manager.freestyle_project_builder \
    .publishers_generator import PublishersGenerator
from jenkins_job_manager.freestyle_project_builder.triggers_generator import \
    TriggersGenerator
from jenkins_job_manager.general_markup_generator import GeneralMarkupGenerator
from jenkins_job_manager.helper import Helper
from jenkins_job_manager.project_builder import ProjectBuilder


class FreestyleProjectBuilder(ProjectBuilder):
    @property
    def repository_type(self) -> str:
        return self._repository_type

    @repository_type.getter
    def repository_type(self) -> str:
        return self._repository_type

    @repository_type.setter
    def repository_type(self, value: str) -> None:
        self._repository_type = value

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
    def junit(self) -> str:
        return self._junit

    @junit.getter
    def junit(self) -> str:
        return self._junit

    @junit.setter
    def junit(self, value: str) -> None:
        self._junit = value

    @property
    def checkstyle(self) -> str:
        return ''

    @checkstyle.getter
    def checkstyle(self) -> str:
        return self._checkstyle

    @checkstyle.setter
    def checkstyle(self, value: str) -> None:
        self._checkstyle = value

    @property
    def hypertext_report(self) -> str:
        return ''

    @hypertext_report.getter
    def hypertext_report(self) -> str:
        return self._hypertext_report

    @hypertext_report.setter
    def hypertext_report(self, value: str) -> None:
        self._hypertext_report = value

    @property
    def recipients(self) -> str:
        return ''

    @recipients.getter
    def recipients(self) -> str:
        return self._recipients

    @recipients.setter
    def recipients(self, value: str) -> None:
        self._recipients = value

    @property
    def jacoco(self) -> bool:
        return False

    @jacoco.getter
    def jacoco(self) -> bool:
        return self._jacoco

    @jacoco.setter
    def jacoco(self, value: bool) -> None:
        self._jacoco = value

    def __init__(self):
        super().__init__()
        self.repository_type = ''
        self.labels = ''
        self.build_command = ''
        self.junit = ''
        self.checkstyle = ''
        self.hypertext_report = ''
        self.recipients = ''
        self.jacoco = ''

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
                locator=self.repository_locator,
                repository_type=self.repository_type
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

    def _append_publishers(self, element: Element) -> None:
        publishers = Element('publishers')
        PublishersGenerator.append_junit_publisher(
            element=publishers,
            junit=self.junit
        )
        PublishersGenerator.append_checkstyle_publisher(
            element=publishers,
            checkstyle=self.checkstyle
        )
        PublishersGenerator.append_jacoco_publisher(
            element=publishers,
            jacoco=self.jacoco
        )
        PublishersGenerator.append_hypertext_report(
            element=publishers,
            hypertext_report=self.hypertext_report
        )
        publishers.append(MailerGenerator.generate(recipients=self.recipients))
        element.append(publishers)

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
        self._append_publishers(element=project)
        project.append(Element('buildWrappers'))

        return project
