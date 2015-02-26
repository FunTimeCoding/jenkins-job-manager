"""Main module of this program."""
import argparse
from lxml import etree
from lxml.etree import Element


class JenkinsJobManager:
    """Take program arguments and generate XML output."""

    def __init__(self, arguments: list):
        """
        :type self: JenkinsJobManager
        :type arguments: list
        :param arguments:
        """
        args = self.parse_args(arguments)

        self.verbose = args.verbose
        self.repo_type = args.type
        self.url = args.url

        if self.is_valid_repo_type(self.repo_type) is False:
            self.repo_type = self.guess_repo_type(self.url)

        if self.verbose is True:
            print('Repository type: ' + self.repo_type)
            print('URL: ' + self.url)

    def run(self) -> int:
        """
        :type self: JenkinsJobManager
        :return:
        """
        print(self.create_xml(url=self.url, repo_type=self.repo_type))
        return 0

    @staticmethod
    def get_valid_repo_types() -> list:
        """
        :rtype : list
        :return:
        """
        return ['svn', 'git']

    @staticmethod
    def is_valid_repo_type(repo_type: str) -> bool:
        """
        :type repo_type: str
        :param repo_type:
        :return:
        """
        return repo_type in JenkinsJobManager.get_valid_repo_types()

    @staticmethod
    def guess_repo_type(url: str) -> str:
        """
        :type url: str
        :param url:
        :return:
        """
        for valid_type in JenkinsJobManager.get_valid_repo_types():
            if valid_type in url:
                return valid_type
        return ''

    @staticmethod
    def parse_args(arguments: list=None) -> argparse.Namespace:
        """
        :type arguments: list
        :param arguments:
        :return:
        """
        description = 'Generate a config.xml for jenkins jobs.'
        parser = argparse.ArgumentParser(description=description)

        required_group = parser.add_argument_group('required named arguments')
        required_group.add_argument(
            '-u',
            '--url',
            help='URL to the repository to check out on Jenkins',
            default=''
        )

        repo_types = ', '.join(JenkinsJobManager.get_valid_repo_types())
        parser.add_argument(
            '-t',
            '--type',
            help='Repository type. Supported: ' + repo_types,
            choices=JenkinsJobManager.get_valid_repo_types(),
            default=''
        )

        parser.add_argument(
            '-v',
            '--verbose',
            help='Turn on some verbose messages.',
            action='store_true'
        )

        return parser.parse_args(arguments)

    @staticmethod
    def create_xml(url: str='', repo_type: str='') -> str:
        """
        :type repo_type: str
        :type url: str
        :param url:
        :param repo_type:
        :return:
        """
        root = Element('project')
        root.append(Element('actions'))
        root.append(Element('description'))

        dependencies = Element('keepDependencies')
        dependencies.text = 'false'
        root.append(dependencies)

        root.append(Element('properties'))

        scm = Element('scm')
        if repo_type is 'git':
            scm.set('class', 'hudson.plugins.git.GitSCM')
            scm.set('plugin', 'git@2.3.2')

            generator = GitXmlGenerator()
            scm.append(generator.generate_version())
            scm.append(generator.generate_remote_config(url))
            scm.append(generator.generate_branches())
            scm.append(generator.generate_do_submodules())
            scm.append(generator.generate_submodule_configs())
            scm.append(Element('extensions'))
        elif repo_type is 'svn':
            scm.set('class', 'hudson.scm.SubversionSCM')
            scm.set('plugin', 'subversion@2.4.5')

            generator = SvnXmlGenerator()
            scm.append(generator.generate_locations(url))
            scm.append(Element('excludedRegions'))
            scm.append(Element('includedRegions'))
            scm.append(Element('excludedUsers'))
            scm.append(Element('excludedRevprop'))
            scm.append(Element('excludedCommitMessages'))
            scm.append(generator.generate_updater())
            scm.append(generator.generate_ignore_changes())
            scm.append(generator.generate_filter_changes())
        else:
            scm.set('class', 'hudson.scm.NullSCM')

        root.append(scm)

        roam = Element('canRoam')
        roam.text = 'true'
        root.append(roam)

        disabled = Element('disabled')
        disabled.text = 'false'
        root.append(disabled)

        upstream = Element('blockBuildWhenDownstreamBuilding')
        upstream.text = 'false'
        root.append(upstream)

        downstream = Element('blockBuildWhenUpstreamBuilding')
        downstream.text = 'false'
        root.append(downstream)

        root.append(Element('triggers'))

        concurrent = Element('concurrentBuild')
        concurrent.text = 'false'
        root.append(concurrent)

        root.append(Element('builders'))
        root.append(Element('publishers'))
        root.append(Element('buildWrappers'))
        mine_serialized = etree.tostring(root,
                                         encoding='unicode',
                                         pretty_print=True)

        return mine_serialized


class GitXmlGenerator:
    """Generate Git specific XML output."""

    @staticmethod
    def generate_remote_config(url: str) -> Element:
        """
        :type url: str
        :param url:
        :return:
        """
        remote_config = Element('userRemoteConfigs')
        git_remote_config_tag = 'hudson.plugins.git.UserRemoteConfig'
        git_remote_config = Element(git_remote_config_tag)
        url_element = Element('url')
        url_element.text = url
        git_remote_config.append(url_element)
        remote_config.append(git_remote_config)
        return remote_config

    @staticmethod
    def generate_branches() -> Element:
        """
        :return:
        """
        branches = Element('branches')
        branch_spec = Element('hudson.plugins.git.BranchSpec')
        branch_spec_name = Element('name')
        branch_spec_name.text = '*/master'
        branch_spec.append(branch_spec_name)
        branches.append(branch_spec)
        return branches

    @staticmethod
    def generate_version() -> Element:
        """
        :return:
        """
        version = Element('configVersion')
        version.text = '2'
        return version

    @staticmethod
    def generate_do_submodules() -> Element:
        """
        :return:
        """
        generate_tag = 'doGenerateSubmoduleConfigurations'
        generate_submodule_configs = Element(generate_tag)
        generate_submodule_configs.text = 'false'
        return generate_submodule_configs

    @staticmethod
    def generate_submodule_configs() -> Element:
        """
        :return:
        """
        submodule_configs = Element('submoduleCfg')
        submodule_configs.set('class', 'list')
        return submodule_configs


class SvnXmlGenerator:
    """Generate Subversion specific XML output."""

    @staticmethod
    def generate_locations(url: str) -> Element:
        """
        :type url: str
        :param url:
        :return:
        """
        locations = Element('locations')

        module_tag = 'hudson.scm.SubversionSCM_-ModuleLocation'
        module_location = Element(module_tag)

        remote = Element('remote')
        remote.text = url
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
        """
        :return:
        """
        updater = Element('workspaceUpdater')
        updater.set('class', 'hudson.scm.subversion.UpdateUpdater')
        return updater

    @staticmethod
    def generate_ignore_changes() -> Element:
        """
        :return:
        """
        ignore_changes = Element('ignoreDirPropChanges')
        ignore_changes.text = 'false'
        return ignore_changes

    @staticmethod
    def generate_filter_changes() -> Element:
        """
        :return:
        """
        filter_changes = Element('filterChangelog')
        filter_changes.text = 'false'
        return filter_changes
