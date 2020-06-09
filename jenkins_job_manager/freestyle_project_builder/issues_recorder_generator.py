from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class IssuesRecorderGenerator:
    @staticmethod
    def create_analysis_tools(checkstyle: str) -> Element:
        analysis_tools = Element('analysisTools')
        check_style = Element(
            'io.jenkins.plugins.analysis.warnings.checkstyle.CheckStyle'
        )
        check_style.append(Element('id'))
        check_style.append(Element('name'))
        check_style.append(
            Helper.create_element_with_text(
                tag='pattern',
                text=checkstyle
            )
        )
        check_style.append(Element('reportEncoding'))
        check_style.append(
            Helper.create_false_boolean_element(tag='skipSymbolicLinks')
        )
        analysis_tools.append(check_style)

        return analysis_tools

    @staticmethod
    def create_minimum_severity() -> Element:
        minimum_severity = Helper.create_plugin_element(
            tag='minimumSeverity',
            plugin='analysis-model-api',
            version='8.1.3',
        )
        minimum_severity.append(
            Helper.create_element_with_text(
                tag='name',
                text='LOW'
            )
        )

        return minimum_severity

    @staticmethod
    def append_source(element: Element) -> None:
        element.append(Element('sourceCodeEncoding'))
        element.append(Element('sourceDirectory'))

    @staticmethod
    def append_ignores(element: Element) -> None:
        element.append(
            Helper.create_false_boolean_element(tag='ignoreQualityGate')
        )
        element.append(
            Helper.create_true_boolean_element(tag='ignoreFailedBuilds')
        )

    @staticmethod
    def append_health_limits(element: Element) -> None:
        element.append(
            Helper.create_element_with_integer(
                tag='healthy',
                integer=0
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='unhealthy',
                integer=0
            )
        )

    @staticmethod
    def append_boolean_flags(element: Element) -> None:
        element.append(
            Helper.create_false_boolean_element(tag='isEnabledForFailure')
        )
        element.append(
            Helper.create_false_boolean_element(tag='isAggregatingResults')
        )
        element.append(
            Helper.create_false_boolean_element(tag='isBlameDisabled')
        )
        element.append(
            Helper.create_false_boolean_element(tag='isForensicsDisabled')
        )

    @staticmethod
    def append_nodes(element: Element) -> None:
        IssuesRecorderGenerator.append_source(element=element)
        IssuesRecorderGenerator.append_ignores(element=element)
        element.append(Element('referenceJobName'))
        element.append(
            Helper.create_false_boolean_element(tag='failOnError')
        )

    @staticmethod
    def append_more_nodes(element: Element) -> None:
        IssuesRecorderGenerator.append_health_limits(element=element)
        element.append(
            IssuesRecorderGenerator.create_minimum_severity()
        )
        element.append(Element('filters'))
        IssuesRecorderGenerator.append_boolean_flags(element=element)
        element.append(Element('qualityGates'))
        element.append(
            Helper.create_element_with_text(
                tag='trendChartType',
                text='AGGREGATION_TOOLS'
            )
        )

    @staticmethod
    def generate(checkstyle: str) -> Element:
        generator = Helper.create_plugin_element(
            tag='io.jenkins.plugins.analysis.core.steps.IssuesRecorder',
            plugin='warnings-ng',
            version='8.1.0',
        )
        generator.append(
            IssuesRecorderGenerator.create_analysis_tools(
                checkstyle=checkstyle
            )
        )
        IssuesRecorderGenerator.append_nodes(element=generator)
        IssuesRecorderGenerator.append_more_nodes(element=generator)

        return generator
