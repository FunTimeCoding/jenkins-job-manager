from sys import argv as argument_vector, exit as system_exit

from lxml.etree import Element

from jenkins_job_manager.custom_argument_parser import CustomArgumentParser
from jenkins_job_manager.lxml_helper import serialize_element


class JenkinsJobManager:
    def __init__(self, arguments: list):
        parsed_arguments = self.get_parser().parse_args(arguments)
        self.repo_type = parsed_arguments.type
        self.locator = parsed_arguments.locator
        self.build_command = parsed_arguments.build_command
        self.description = parsed_arguments.description
        self.junit = parsed_arguments.junit
        self.hypertext_report = parsed_arguments.hypertext_report
        self.checkstyle = parsed_arguments.checkstyle
        self.jacoco = parsed_arguments.jacoco
        self.recipients = parsed_arguments.recipients
        self.labels = parsed_arguments.labels

        if self.is_valid_repo_type(self.repo_type) is False:
            self.repo_type = self.guess_repo_type(self.locator)

    @staticmethod
    def main():
        system_exit(JenkinsJobManager(argument_vector[1:]).run())

    def run(self) -> int:
        print("<?xml version='1.1' encoding='UTF-8'?>")
        print(self.generate_serialized_xml().strip())

        return 0

    @staticmethod
    def get_valid_repo_types() -> list:
        return ['svn', 'git']

    @staticmethod
    def is_valid_repo_type(repo_type: str) -> bool:
        return repo_type in JenkinsJobManager.get_valid_repo_types()

    @staticmethod
    def guess_repo_type(locator: str) -> str:
        repo_type = ''

        for valid_type in JenkinsJobManager.get_valid_repo_types():
            if valid_type in locator:
                repo_type = valid_type
                break

        return repo_type

    @staticmethod
    def get_parser() -> CustomArgumentParser:
        description = 'Generate a config.xml for Jenkins jobs.'
        parser = CustomArgumentParser(description=description)

        required_group = parser.add_argument_group('required named arguments')
        required_group.add_argument(
            '--locator',
            help='locator to the repository to check out on Jenkins',
            required=True
        )

        parser.add_argument(
            '--type',
            help='Repository type.',
            choices=JenkinsJobManager.get_valid_repo_types()
        )
        parser.add_argument(
            '--build-command',
            help='Set the build command.',
            default=''
        )
        parser.add_argument(
            '--junit',
            help='Set the JUnit output to publish.',
            default=''
        )
        parser.add_argument(
            '--hypertext-report',
            help='Set the hypertext report to publish.',
            default=''
        )
        parser.add_argument(
            '--checkstyle',
            help='Set the checkstyle output to publish.',
            default=''
        )
        parser.add_argument(
            '--jacoco',
            help='Enable publishing JaCoCo output.',
            action='store_true'
        )
        parser.add_argument(
            '--description',
            help='Set the job description.',
            default=''
        )
        parser.add_argument(
            '--labels',
            help='Set the job labels.',
            default=''
        )
        parser.add_argument(
            '--recipients',
            help='Set mail recipients in case of build failure, '
                 'whitespace-separated.',
            default=''
        )

        return parser

    def generate_xml(self) -> Element:
        root = Element('project')
        root.append(Element('actions'))
        description = Element('description')
        description.text = self.description
        root.append(description)
        generator = GeneralMarkupGenerator()
        root.append(generator.generate_dependencies())
        root.append(Element('properties'))
        scm = generator.generate_scm_for_repo_type(
            locator=self.locator,
            repo_type=self.repo_type
        )
        root.append(scm)

        if self.labels == '':
            root.append(generator.generate_roam(True))
        else:
            root.append(generator.generate_assigned_node(self.labels))
            root.append(generator.generate_roam(False))

        root.append(generator.generate_disabled())
        root.append(generator.generate_upstream())
        root.append(generator.generate_downstream())
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

        root.append(triggers)
        root.append(generator.generate_concurrent())
        builders = Element('builders')

        if self.build_command != '':
            shell = Element('hudson.tasks.Shell')
            command = Element('command')
            command.text = self.build_command
            shell.append(command)
            builders.append(shell)

        root.append(builders)
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
        root.append(publishers)
        root.append(Element('buildWrappers'))

        return root

    def generate_serialized_xml(self) -> str:
        xml = self.generate_xml()

        return serialize_element(xml)


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


class GeneralMarkupGenerator:
    @staticmethod
    def generate_dependencies() -> Element:
        dependencies = Element('keepDependencies')
        dependencies.text = 'false'

        return dependencies

    @staticmethod
    def generate_roam(enabled: bool) -> Element:
        roam = Element('canRoam')

        if enabled:
            roam.text = 'true'
        else:
            roam.text = 'false'

        return roam

    @staticmethod
    def generate_assigned_node(labels: str) -> Element:
        assigned_node = Element('assignedNode')
        assigned_node.text = labels

        return assigned_node

    @staticmethod
    def generate_disabled() -> Element:
        disabled = Element('disabled')
        disabled.text = 'false'

        return disabled

    @staticmethod
    def generate_upstream() -> Element:
        upstream = Element('blockBuildWhenDownstreamBuilding')
        upstream.text = 'false'

        return upstream

    @staticmethod
    def generate_downstream() -> Element:
        downstream = Element('blockBuildWhenUpstreamBuilding')
        downstream.text = 'false'

        return downstream

    @staticmethod
    def generate_concurrent() -> Element:
        concurrent = Element('concurrentBuild')
        concurrent.text = 'false'

        return concurrent

    @staticmethod
    def generate_scm_for_repo_type(locator: str, repo_type: str) -> Element:
        scm = Element('scm')

        if repo_type == 'git':
            scm.set('class', 'hudson.plugins.git.GitSCM')
            scm.set('plugin', 'git@4.2.2')
            git_generator = GitMarkupGenerator()
            scm.append(git_generator.generate_version())
            scm.append(git_generator.generate_remote_config(locator))
            scm.append(git_generator.generate_branches())
            scm.append(git_generator.generate_do_submodules())
            scm.append(git_generator.generate_submodule_configs())
            scm.append(Element('extensions'))
        elif repo_type == 'svn':
            scm.set('class', 'hudson.scm.SubversionSCM')
            scm.set('plugin', 'subversion@2.4.5')
            svn_generator = SubversionMarkupGenerator()
            scm.append(svn_generator.generate_locations(locator))
            scm.append(Element('excludedRegions'))
            scm.append(Element('includedRegions'))
            scm.append(Element('excludedUsers'))
            scm.append(Element('excludedRevprop'))
            scm.append(Element('excludedCommitMessages'))
            scm.append(svn_generator.generate_updater())
            scm.append(svn_generator.generate_ignore_changes())
            scm.append(svn_generator.generate_filter_changes())
        else:
            scm.set('class', 'hudson.scm.NullSCM')

        return scm


class GitMarkupGenerator:
    @staticmethod
    def generate_remote_config(locator: str) -> Element:
        remote_config = Element('userRemoteConfigs')
        git_remote_config_tag = 'hudson.plugins.git.UserRemoteConfig'
        git_remote_config = Element(git_remote_config_tag)
        locator_element = Element('url')
        locator_element.text = locator
        git_remote_config.append(locator_element)
        remote_config.append(git_remote_config)

        return remote_config

    @staticmethod
    def generate_branches() -> Element:
        branches = Element('branches')
        branch_spec = Element('hudson.plugins.git.BranchSpec')
        branch_spec_name = Element('name')
        branch_spec_name.text = '*/master'
        branch_spec.append(branch_spec_name)
        branches.append(branch_spec)

        return branches

    @staticmethod
    def generate_version() -> Element:
        version = Element('configVersion')
        version.text = '2'

        return version

    @staticmethod
    def generate_do_submodules() -> Element:
        generate_tag = 'doGenerateSubmoduleConfigurations'
        generate_submodule_configs = Element(generate_tag)
        generate_submodule_configs.text = 'false'

        return generate_submodule_configs

    @staticmethod
    def generate_submodule_configs() -> Element:
        submodule_configs = Element('submoduleCfg')
        submodule_configs.set('class', 'list')

        return submodule_configs


class SubversionMarkupGenerator:
    @staticmethod
    def generate_locations(locator: str) -> Element:
        locations = Element('locations')
        module_tag = 'hudson.scm.SubversionSCM_-ModuleLocation'
        module_location = Element(module_tag)
        remote = Element('remote')
        remote.text = locator
        module_location.append(remote)
        module_location.append(Element('credentialsId'))
        local = Element('local')
        local.text = '.'
        module_location.append(local)
        depth = Element('depthOption')
        depth.text = 'infinity'
        module_location.append(depth)
        ignore_externals = Element('ignoreExternalsOption')
        ignore_externals.text = 'true'
        module_location.append(ignore_externals)
        locations.append(module_location)

        return locations

    @staticmethod
    def generate_updater() -> Element:
        updater = Element('workspaceUpdater')
        updater.set('class', 'hudson.scm.subversion.UpdateUpdater')

        return updater

    @staticmethod
    def generate_ignore_changes() -> Element:
        ignore_changes = Element('ignoreDirPropChanges')
        ignore_changes.text = 'false'

        return ignore_changes

    @staticmethod
    def generate_filter_changes() -> Element:
        filter_changes = Element('filterChangelog')
        filter_changes.text = 'false'

        return filter_changes
