from lxml.etree import Element
from python_utility.custom_argument_parser import CustomArgumentParser

from jenkins_job_manager.lxml_helper import serialize_element


class JenkinsJobManager:
    def __init__(self, arguments: list):
        parser = self.get_parser()
        parsed_arguments = parser.parse_args(arguments)
        self.verbose = parsed_arguments.verbose
        self.repo_type = parsed_arguments.type
        self.locator = parsed_arguments.locator
        self.enable_build = parsed_arguments.build
        self.description = parsed_arguments.description

        if self.is_valid_repo_type(self.repo_type) is False:
            self.repo_type = self.guess_repo_type(self.locator)

        if self.verbose is True:
            print('Repository type: ' + self.repo_type)
            print('Enable build: ' + str(self.enable_build))
            print('locator: ' + self.locator)

    def run(self) -> int:
        print("<?xml version='1.0' encoding='UTF-8'?>")
        print(self.generate_serialized_xml().strip())

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
            '--verbose',
            help='Enable verbose messages.',
            action='store_true'
        )
        parser.add_argument(
            '--build',
            help='Generate the build command.',
            action='store_true'
        )
        parser.add_argument(
            '--description',
            help='Add a job description.',
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
        if self.enable_build is True:
            timer_trigger = Element('hudson.triggers.TimerTrigger')
            timer_spec = Element('spec')
            # end of week, friday mornings
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
        if self.enable_build is True:
            shell = Element('hudson.tasks.Shell')
            command = Element('command')
            command.text = "export PYTHONHOME=/usr/local/opt/python3/" \
                           "Frameworks/Python.framework/Versions" \
                           "/3.4\n./build.sh"
            shell.append(command)
            builders.append(shell)

        root.append(builders)
        root.append(Element('publishers'))
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
            scm.set('plugin', 'git@2.5.3')

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
