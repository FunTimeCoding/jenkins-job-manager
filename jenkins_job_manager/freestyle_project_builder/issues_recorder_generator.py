from lxml.etree import Element


class IssuesRecorderGenerator:
    @staticmethod
    def generate_issues_recorder(checkstyle: str) -> Element:
        issues_recorder = Element(
            'io.jenkins.plugins.analysis.core.steps.IssuesRecorder'
        )
        issues_recorder.set('plugin', 'warnings-ng@8.1.0')
        analysis_tools = Element('analysisTools')
        check_style = Element(
            'io.jenkins.plugins.analysis.warnings.checkstyle.CheckStyle'
        )
        identifier = Element('id')
        identifier.text = ''
        check_style.append(identifier)
        name = Element('name')
        name.text = ''
        check_style.append(name)
        pattern = Element('pattern')
        pattern.text = checkstyle
        check_style.append(pattern)
        report_encoding = Element('reportEncoding')
        report_encoding.text = ''
        check_style.append(report_encoding)
        skip_symbolic_links = Element('skipSymbolicLinks')
        skip_symbolic_links.text = 'false'
        check_style.append(skip_symbolic_links)
        analysis_tools.append(check_style)
        issues_recorder.append(analysis_tools)
        source_code_encoding = Element('sourceCodeEncoding')
        source_code_encoding.text = ''
        issues_recorder.append(source_code_encoding)
        source_directory = Element('sourceDirectory')
        source_directory.text = ''
        issues_recorder.append(source_directory)
        ignore_quality_gate = Element('ignoreQualityGate')
        ignore_quality_gate.text = 'false'
        issues_recorder.append(ignore_quality_gate)
        ignore_failed_builds = Element('ignoreFailedBuilds')
        ignore_failed_builds.text = 'true'
        issues_recorder.append(ignore_failed_builds)
        reference_job_name = Element('referenceJobName')
        reference_job_name.text = ''
        issues_recorder.append(reference_job_name)
        fail_on_error = Element('failOnError')
        fail_on_error.text = 'false'
        issues_recorder.append(fail_on_error)
        healthy = Element('healthy')
        healthy.text = '0'
        issues_recorder.append(healthy)
        unhealthy = Element('unhealthy')
        unhealthy.text = '0'
        issues_recorder.append(unhealthy)
        minimum_severity = Element('minimumSeverity')
        minimum_severity.set('plugin', 'analysis-model-api@8.1.3')
        name = Element('name')
        name.text = 'LOW'
        minimum_severity.append(name)
        issues_recorder.append(minimum_severity)
        issues_recorder.append(Element('filters'))
        is_enabled_for_failure = Element('isEnabledForFailure')
        is_enabled_for_failure.text = 'false'
        issues_recorder.append(is_enabled_for_failure)
        is_aggregating_results = Element('isAggregatingResults')
        is_aggregating_results.text = 'false'
        issues_recorder.append(is_aggregating_results)
        is_blame_disabled = Element('isBlameDisabled')
        is_blame_disabled.text = 'false'
        issues_recorder.append(is_blame_disabled)
        is_forensics_disabled = Element('isForensicsDisabled')
        is_forensics_disabled.text = 'false'
        issues_recorder.append(is_forensics_disabled)
        issues_recorder.append(Element('qualityGates'))
        trend_chart_type = Element('trendChartType')
        trend_chart_type.text = 'AGGREGATION_TOOLS'
        issues_recorder.append(trend_chart_type)

        return issues_recorder
