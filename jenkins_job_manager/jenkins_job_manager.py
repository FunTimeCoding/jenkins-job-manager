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
        self.checkstyle = parsed_arguments.checkstyle
        self.recipients = parsed_arguments.recipients

        if self.is_valid_repo_type(self.repo_type) is False:
            self.repo_type = self.guess_repo_type(self.locator)

    @staticmethod
    def main():
        system_exit(JenkinsJobManager(argument_vector[1:]).run())

    def run(self) -> int:
        print("<?xml version='1.0' encoding='UTF-8'?>")
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
            '--checkstyle',
            help='Set the checkstyle output to publish.',
            default=''
        )
        parser.add_argument(
            '--description',
            help='Set the job description.',
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

        if self.description != '':
            description.text = self.description

        root.append(description)
        generator = GenericXmlGenerator()
        root.append(generator.generate_dependencies())
        root.append(Element('properties'))
        scm = generator.generate_scm_for_repo_type(
            locator=self.locator,
            repo_type=self.repo_type
        )
        root.append(scm)
        root.append(generator.generate_roam())
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
            junit.set('plugin', 'junit@1.24')
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
            checkstyle = Element(
                'hudson.plugins.checkstyle.CheckStylePublisher'
            )
            checkstyle.set('plugin', 'checkstyle@3.50')
            checkstyle.append(Element('healthy'))
            checkstyle.append(Element('unHealthy'))
            threshold = Element('thresholdLimit')
            threshold.text = 'low'
            checkstyle.append(threshold)
            name = Element('pluginName')
            # This space belongs here.
            name.text = '[CHECKSTYLE] '
            checkstyle.append(name)
            checkstyle.append(Element('defaultEncoding'))
            run_on_failed = Element('canRunOnFailed')
            run_on_failed.text = 'true'
            checkstyle.append(run_on_failed)
            previous_build_reference = Element('usePreviousBuildAsReference')
            previous_build_reference.text = 'false'
            checkstyle.append(previous_build_reference)
            stable_build_reference = Element('useStableBuildAsReference')
            stable_build_reference.text = 'false'
            checkstyle.append(stable_build_reference)
            delta_values = Element('useDeltaValues')
            delta_values.text = 'false'
            checkstyle.append(delta_values)
            thresholds = Element('thresholds')
            thresholds.set('plugin', 'analysis-core@1.94')
            unstable_total_all = Element('unstableTotalAll')
            thresholds.append(unstable_total_all)
            unstable_total_high = Element('unstableTotalHigh')
            thresholds.append(unstable_total_high)
            unstable_total_normal = Element('unstableTotalNormal')
            thresholds.append(unstable_total_normal)
            unstable_total_low = Element('unstableTotalLow')
            thresholds.append(unstable_total_low)
            unstable_new_all = Element('unstableNewAll')
            thresholds.append(unstable_new_all)
            unstable_new_high = Element('unstableNewHigh')
            thresholds.append(unstable_new_high)
            unstable_new_normal = Element('unstableNewNormal')
            thresholds.append(unstable_new_normal)
            unstable_new_low = Element('unstableNewLow')
            thresholds.append(unstable_new_low)
            failed_total_all = Element('failedTotalAll')
            thresholds.append(failed_total_all)
            failed_total_high = Element('failedTotalHigh')
            thresholds.append(failed_total_high)
            failed_total_normal = Element('failedTotalNormal')
            thresholds.append(failed_total_normal)
            failed_total_low = Element('failedTotalLow')
            thresholds.append(failed_total_low)
            failed_new_all = Element('failedNewAll')
            thresholds.append(failed_new_all)
            failed_new_high = Element('failedNewHigh')
            thresholds.append(failed_new_high)
            failed_new_normal = Element('failedNewNormal')
            thresholds.append(failed_new_normal)
            failed_new_low = Element('failedNewLow')
            thresholds.append(failed_new_low)
            checkstyle.append(thresholds)
            detect_modules = Element('shouldDetectModules')
            detect_modules.text = 'false'
            checkstyle.append(detect_modules)
            compute = Element('dontComputeNew')
            compute.text = 'true'
            checkstyle.append(compute)
            relative_paths = Element('doNotResolveRelativePaths')
            relative_paths.text = 'false'
            checkstyle.append(relative_paths)
            pattern = Element('pattern')
            pattern.text = self.checkstyle
            checkstyle.append(pattern)
            publishers.append(checkstyle)

        mailer = Element(
            'hudson.tasks.Mailer'
        )
        mailer.set('plugin', 'mailer@1.20')
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


class GenericXmlGenerator:
    @staticmethod
    def generate_dependencies() -> Element:
        dependencies = Element('keepDependencies')
        dependencies.text = 'false'

        return dependencies

    @staticmethod
    def generate_roam() -> Element:
        roam = Element('canRoam')
        roam.text = 'true'

        return roam

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
            scm.set('plugin', 'git@3.7.0')
            git_generator = GitXmlGenerator()
            scm.append(git_generator.generate_version())
            scm.append(git_generator.generate_remote_config(locator))
            scm.append(git_generator.generate_branches())
            scm.append(git_generator.generate_do_submodules())
            scm.append(git_generator.generate_submodule_configs())
            scm.append(Element('extensions'))
        elif repo_type == 'svn':
            scm.set('class', 'hudson.scm.SubversionSCM')
            scm.set('plugin', 'subversion@2.4.5')
            svn_generator = SvnXmlGenerator()
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


class GitXmlGenerator:
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


class SvnXmlGenerator:
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
