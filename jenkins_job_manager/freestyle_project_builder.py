from lxml.etree import Element

from jenkins_job_manager.general_markup_generator import GeneralMarkupGenerator
from jenkins_job_manager.project_builder import ProjectBuilder
from jenkins_job_manager.publisher_markup_generator import \
    PublisherMarkupGenerator


class FreestyleProjectBuilder(ProjectBuilder):
    @property
    def repository_type(self) -> str:
        return ''

    @property
    def labels(self) -> str:
        return ''

    @property
    def build_command(self) -> str:
        return ''

    @property
    def junit(self) -> str:
        return ''

    @property
    def checkstyle(self) -> str:
        return ''

    @property
    def hypertext_report(self) -> str:
        return ''

    @property
    def recipients(self) -> str:
        return ''

    @property
    def jacoco(self) -> bool:
        return False

    @repository_type.setter
    def repository_type(self, value: str) -> None:
        self._repository_type = value

    @repository_type.getter
    def repository_type(self) -> str:
        return self._repository_type

    @labels.setter
    def labels(self, value: str) -> None:
        self._labels = value

    @labels.getter
    def labels(self) -> str:
        return self._labels

    @build_command.setter
    def build_command(self, value: str) -> None:
        self._build_command = value

    @build_command.getter
    def build_command(self) -> str:
        return self._build_command

    @junit.setter
    def junit(self, value: str) -> None:
        self._junit = value

    @junit.getter
    def junit(self) -> str:
        return self._junit

    @checkstyle.setter
    def checkstyle(self, value: str) -> None:
        self._checkstyle = value

    @checkstyle.getter
    def checkstyle(self) -> str:
        return self._checkstyle

    @hypertext_report.setter
    def hypertext_report(self, value: str) -> None:
        self._hypertext_report = value

    @hypertext_report.getter
    def hypertext_report(self) -> str:
        return self._hypertext_report

    @recipients.setter
    def recipients(self, value: str) -> None:
        self._recipients = value

    @recipients.getter
    def recipients(self) -> str:
        return self._recipients

    @jacoco.setter
    def jacoco(self, value: bool) -> None:
        self._jacoco = value

    @jacoco.getter
    def jacoco(self) -> bool:
        return self._jacoco

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

    def build(self) -> Element:
        project = Element('project')
        project.append(Element('actions'))
        description = Element('description')
        description.text = self.description
        project.append(description)
        generator = GeneralMarkupGenerator()
        project.append(generator.generate_dependencies())
        project.append(Element('properties'))
        scm = generator.generate_scm_for_repository_type(
            locator=self.repository_locator,
            repository_type=self.repository_type
        )
        project.append(scm)

        if self.labels == '':
            project.append(generator.generate_roam(True))
        else:
            project.append(generator.generate_assigned_node(self.labels))
            project.append(generator.generate_roam(False))

        project.append(generator.generate_disabled())
        project.append(generator.generate_upstream())
        project.append(generator.generate_downstream())
        triggers = Element('triggers')

        if self.build_command != '':
            timer_trigger = Element('hudson.triggers.TimerTrigger')
            timer_spec = Element('spec')
            # end of week, Friday mornings
            timer_spec.text = 'H 6 * * 5'
            # end of day, mornings
            # timer_spec.text = 'H 6 * * 1-5'
            timer_trigger.append(timer_spec)
            triggers.append(timer_trigger)
            scm_trigger = Element('hudson.triggers.SCMTrigger')
            scm_spec = Element('spec')
            scm_spec.text = 'H/30 * * * *'
            scm_trigger.append(scm_spec)
            hooks = Element('ignorePostCommitHooks')
            hooks.text = 'false'
            scm_trigger.append(hooks)
            triggers.append(scm_trigger)

        project.append(triggers)
        project.append(generator.generate_concurrent())
        builders = Element('builders')

        if self.build_command != '':
            shell = Element('hudson.tasks.Shell')
            command = Element('command')
            command.text = self.build_command
            shell.append(command)
            builders.append(shell)

        project.append(builders)
        publishers = Element('publishers')

        if self.junit != '':
            junit = Element('hudson.tasks.junit.JUnitResultArchiver')
            junit.set('plugin', 'junit@1.29')
            results = Element('testResults')
            results.text = self.junit
            junit.append(results)
            keep_long_output = Element('keepLongStdio')
            keep_long_output.text = 'false'
            junit.append(keep_long_output)
            health_factor = Element('healthScaleFactor')
            health_factor.text = '1.0'
            junit.append(health_factor)
            allow_empty = Element('allowEmptyResults')
            allow_empty.text = 'false'
            junit.append(allow_empty)
            publishers.append(junit)

        if self.checkstyle != '':
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
            pattern.text = self.checkstyle
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
            publishers.append(issues_recorder)

        if self.jacoco:
            jacoco_publisher = Element(
                'hudson.plugins.jacoco.JacocoPublisher'
            )
            jacoco_publisher.set('plugin', 'jacoco@3.0.5')
            exec_pattern = Element('execPattern')
            exec_pattern.text = '**/**.exec'
            jacoco_publisher.append(exec_pattern)
            class_pattern = Element('classPattern')
            class_pattern.text = '**/classes'
            jacoco_publisher.append(class_pattern)
            source_pattern = Element('sourcePattern')
            source_pattern.text = '**/src/main/java'
            jacoco_publisher.append(source_pattern)
            source_inclusion_pattern = Element('sourceInclusionPattern')
            source_inclusion_pattern.text = '**/*.java,**/*.groovy,**/*.kt,**/*.kts'
            jacoco_publisher.append(source_inclusion_pattern)
            source_exclusion_pattern = Element('sourceExclusionPattern')
            source_exclusion_pattern.text = ''
            jacoco_publisher.append(source_exclusion_pattern)
            inclusion_pattern = Element('inclusionPattern')
            inclusion_pattern.text = ''
            jacoco_publisher.append(inclusion_pattern)
            exclusion_pattern = Element('exclusionPattern')
            exclusion_pattern.text = ''
            jacoco_publisher.append(exclusion_pattern)
            skip_copy_of_source_files = Element('skipCopyOfSrcFiles')
            skip_copy_of_source_files.text = 'false'
            jacoco_publisher.append(skip_copy_of_source_files)
            minimum_instruction_coverage = Element('minimumInstructionCoverage')
            minimum_instruction_coverage.text = '0'
            jacoco_publisher.append(minimum_instruction_coverage)
            minimum_branch_coverage = Element('minimumBranchCoverage')
            minimum_branch_coverage.text = '0'
            jacoco_publisher.append(minimum_branch_coverage)
            minimum_complexity_coverage = Element('minimumComplexityCoverage')
            minimum_complexity_coverage.text = '0'
            jacoco_publisher.append(minimum_complexity_coverage)
            minimum_line_coverage = Element('minimumLineCoverage')
            minimum_line_coverage.text = '0'
            jacoco_publisher.append(minimum_line_coverage)
            minimum_method_coverage = Element('minimumMethodCoverage')
            minimum_method_coverage.text = '0'
            jacoco_publisher.append(minimum_method_coverage)
            minimum_class_coverage = Element('minimumClassCoverage')
            minimum_class_coverage.text = '0'
            jacoco_publisher.append(minimum_class_coverage)
            maximum_instruction_coverage = Element('maximumInstructionCoverage')
            maximum_instruction_coverage.text = '0'
            jacoco_publisher.append(maximum_instruction_coverage)
            maximum_branch_coverage = Element('maximumBranchCoverage')
            maximum_branch_coverage.text = '0'
            jacoco_publisher.append(maximum_branch_coverage)
            maximum_complexity_coverage = Element('maximumComplexityCoverage')
            maximum_complexity_coverage.text = '0'
            jacoco_publisher.append(maximum_complexity_coverage)
            maximum_line_coverage = Element('maximumLineCoverage')
            maximum_line_coverage.text = '0'
            jacoco_publisher.append(maximum_line_coverage)
            maximum_method_coverage = Element('maximumMethodCoverage')
            maximum_method_coverage.text = '0'
            jacoco_publisher.append(maximum_method_coverage)
            maximum_class_coverage = Element('maximumClassCoverage')
            maximum_class_coverage.text = '0'
            jacoco_publisher.append(maximum_class_coverage)
            change_build_status = Element('changeBuildStatus')
            change_build_status.text = 'false'
            jacoco_publisher.append(change_build_status)
            run_always = Element('runAlways')
            run_always.text = 'false'
            jacoco_publisher.append(run_always)
            delta_instruction_coverage = Element('deltaInstructionCoverage')
            delta_instruction_coverage.text = '0'
            jacoco_publisher.append(delta_instruction_coverage)
            delta_branch_coverage = Element('deltaBranchCoverage')
            delta_branch_coverage.text = '0'
            jacoco_publisher.append(delta_branch_coverage)
            delta_complexity_coverage = Element('deltaComplexityCoverage')
            delta_complexity_coverage.text = '0'
            jacoco_publisher.append(delta_complexity_coverage)
            delta_line_coverage = Element('deltaLineCoverage')
            delta_line_coverage.text = '0'
            jacoco_publisher.append(delta_line_coverage)
            delta_method_coverage = Element('deltaMethodCoverage')
            delta_method_coverage.text = '0'
            jacoco_publisher.append(delta_method_coverage)
            delta_class_coverage = Element('deltaClassCoverage')
            delta_class_coverage.text = '0'
            jacoco_publisher.append(delta_class_coverage)
            build_over_build = Element('buildOverBuild')
            build_over_build.text = 'false'
            jacoco_publisher.append(build_over_build)
            publishers.append(jacoco_publisher)

        if self.hypertext_report != '':
            hypertext_report = PublisherMarkupGenerator.generate_hypertext(
                hypertext_report=self.hypertext_report
            )
            publishers.append(hypertext_report)

        mailer = Element(
            'hudson.tasks.Mailer'
        )
        mailer.set('plugin', 'mailer@1.32')
        recipients = Element('recipients')

        if self.recipients != '':
            recipients.text = self.recipients

        mailer.append(recipients)
        every_unstable_build = Element('dontNotifyEveryUnstableBuild')
        every_unstable_build.text = 'false'
        mailer.append(every_unstable_build)
        individuals = Element('sendToIndividuals')
        individuals.text = 'true'
        mailer.append(individuals)
        publishers.append(mailer)
        project.append(publishers)
        project.append(Element('buildWrappers'))

        return project
