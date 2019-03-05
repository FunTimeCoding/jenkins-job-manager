from lxml.etree import Element


class PublisherMarkupGenerator:
    @staticmethod
    def generate_hypertext(hypertext_report: str) -> Element:
        hypertext_report_element = Element(
            'htmlpublisher.HtmlPublisher'
        )
        hypertext_report_element.set('plugin', 'htmlpublisher@1.16')

        report_targets = Element('reportTargets')
        hypertext_publisher_target = Element(
            'htmlpublisher.HtmlPublisherTarget'
        )

        report_name = Element('reportName')
        report_name.text = hypertext_report.replace(
            '_',
            ' '
        ).title() + ' Report'
        hypertext_publisher_target.append(report_name)

        report_directory = Element('reportDir')
        report_directory.text = 'build/log/' + hypertext_report
        hypertext_publisher_target.append(report_directory)

        report_files = Element('reportFiles')
        report_files.text = 'index.html'
        hypertext_publisher_target.append(report_files)

        always_link_to_last_build = Element('alwaysLinkToLastBuild')
        always_link_to_last_build.text = 'false'
        hypertext_publisher_target.append(always_link_to_last_build)

        hypertext_publisher_target.append(Element('reportTitles'))

        keep_all = Element('keepAll')
        keep_all.text = 'false'
        hypertext_publisher_target.append(keep_all)

        allow_missing = Element('allowMissing')
        allow_missing.text = 'false'
        hypertext_publisher_target.append(allow_missing)

        includes = Element('includes')
        includes.text = '**/*'
        hypertext_publisher_target.append(includes)

        report_targets.append(hypertext_publisher_target)
        hypertext_report_element.append(report_targets)

        return hypertext_report_element
