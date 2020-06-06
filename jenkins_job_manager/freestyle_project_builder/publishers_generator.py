from lxml.etree import Element

from jenkins_job_manager.freestyle_project_builder.issues_recorder_generator \
    import IssuesRecorderGenerator
from jenkins_job_manager.freestyle_project_builder \
    .java_code_coverage_publisher import JavaCodeCoveragePublisher
from jenkins_job_manager.freestyle_project_builder.junit_result_archiver \
    import JUnitResultArchiver
from jenkins_job_manager.freestyle_project_builder.mailer_generator \
    import MailerGenerator
from jenkins_job_manager.markup_publisher_generator import \
    MarkupPublisherGenerator


class PublishersGenerator:
    @staticmethod
    def append_junit_publisher(parent: Element, junit: str) -> None:
        if junit:
            parent.append(
                JUnitResultArchiver.generate(result_path=junit)
            )

    @staticmethod
    def append_checkstyle_publisher(parent: Element, checkstyle: str) -> None:
        if checkstyle:
            parent.append(
                IssuesRecorderGenerator.generate(checkstyle=checkstyle)
            )

    @staticmethod
    def append_jacoco_publisher(parent: Element, jacoco: bool) -> None:
        if jacoco:
            parent.append(JavaCodeCoveragePublisher.generate())

    @staticmethod
    def append_hypertext_report(
            parent: Element,
            hypertext_report: str
    ) -> None:
        if hypertext_report:
            parent.append(
                MarkupPublisherGenerator.generate(
                    hypertext_report=hypertext_report,
                )
            )

    @staticmethod
    def append_recipients(
            parent: Element,
            recipients: str
    ) -> None:
        parent.append(
            MailerGenerator.generate(
                recipients=recipients,
            )
        )
