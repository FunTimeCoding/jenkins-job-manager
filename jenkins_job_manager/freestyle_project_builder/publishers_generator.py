from lxml.etree import Element

from jenkins_job_manager.freestyle_project_builder.issues_recorder_generator \
    import IssuesRecorderGenerator
from jenkins_job_manager.freestyle_project_builder \
    .java_code_coverage_publisher import JavaCodeCoveragePublisher
from jenkins_job_manager.freestyle_project_builder.junit_result_archiver \
    import JUnitResultArchiver
from jenkins_job_manager.markup_publisher_generator import \
    MarkupPublisherGenerator


class PublishersGenerator:
    @staticmethod
    def append_junit_publisher(element: Element, junit: str) -> None:
        if junit:
            element.append(
                JUnitResultArchiver.generate(result_path=junit)
            )

    @staticmethod
    def append_checkstyle_publisher(element: Element, checkstyle: str) -> None:
        if checkstyle:
            element.append(
                IssuesRecorderGenerator.generate(checkstyle=checkstyle)
            )

    @staticmethod
    def append_jacoco_publisher(element: Element, jacoco: bool) -> None:
        if jacoco:
            element.append(JavaCodeCoveragePublisher.generate())

    @staticmethod
    def append_hypertext_report(
            element: Element,
            hypertext_report: str
    ) -> None:
        if hypertext_report:
            element.append(
                MarkupPublisherGenerator.generate(
                    hypertext_report=hypertext_report
                )
            )
