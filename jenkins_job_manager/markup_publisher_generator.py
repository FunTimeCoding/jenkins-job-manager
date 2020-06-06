from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class MarkupPublisherGenerator:
    @staticmethod
    def generate(hypertext_report: str) -> Element:
        publisher = Helper.create_plugin_element(
            tag='htmlpublisher.HtmlPublisher',
            plugin='htmlpublisher',
            version='1.16',
        )
        report_targets = Element('reportTargets')
        target = Element(
            'htmlpublisher.HtmlPublisherTarget'
        )
        MarkupPublisherGenerator._append_targets(
            element=target,
            hypertext_report=hypertext_report,
        )
        report_targets.append(target)
        publisher.append(report_targets)

        return publisher

    @staticmethod
    def _append_targets(element: Element, hypertext_report: str) -> None:
        element.append(
            Helper.create_element_with_text(
                tag='reportName',
                text=hypertext_report.replace(
                    '_',
                    ' '
                ).title() + ' Report'
            )
        )
        element.append(
            Helper.create_element_with_text(
                tag='reportDir',
                text='build/log/' + hypertext_report
            )
        )
        element.append(
            Helper.create_element_with_text(
                tag='reportFiles',
                text='index.html'
            )
        )
        element.append(
            Helper.create_false_boolean_element(tag='alwaysLinkToLastBuild')
        )
        element.append(Element('reportTitles'))
        element.append(Helper.create_false_boolean_element(tag='keepAll'))
        element.append(Helper.create_false_boolean_element(tag='allowMissing'))
        element.append(
            Helper.create_element_with_text(
                tag='includes',
                text='**/*'
            )
        )
