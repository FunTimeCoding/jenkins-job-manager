import argparse
from lxml import etree


class JenkinsJobManager:
    def __init__(self, arguments: list):
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
        print(self.create_xml(url=self.url, repo_type=self.repo_type))
        return 0

    @staticmethod
    def get_valid_repo_types() -> list:
        return ['svn', 'git']

    @staticmethod
    def is_valid_repo_type(repo_type: str) -> bool:
        return repo_type in JenkinsJobManager.get_valid_repo_types()

    @staticmethod
    def guess_repo_type(url: str) -> str:
        for valid_type in JenkinsJobManager.get_valid_repo_types():
            if valid_type in url:
                return valid_type
        return ''

    @staticmethod
    def parse_args(arguments: list=None) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Generate a config.xml for jenkins jobs.')

        required_group = parser.add_argument_group('required named arguments')
        required_group.add_argument(
            '-u',
            '--url',
            help='URL to the repository to check out on Jenkins',
            default=''
        )

        parser.add_argument(
            '-t',
            '--type',
            help='Repository type. Supported: ' + ', '.join(JenkinsJobManager.get_valid_repo_types()),
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
        root = etree.Element('project')
        root.append(etree.Element('actions'))
        root.append(etree.Element('description'))

        dependencies = etree.Element('keepDependencies')
        dependencies.text = 'false'
        root.append(dependencies)

        root.append(etree.Element('properties'))

        scm = etree.Element('scm')
        if repo_type is 'git':
            scm.set('class', 'hudson.plugins.git.GitSCM')
            scm.set('plugin', 'git@2.3.2')

            version = etree.Element('configVersion')
            version.text = '2'
            scm.append(version)

            remote_config = etree.Element('userRemoteConfigs')
            git_remote_config = etree.Element('hudson.plugins.git.UserRemoteConfig')
            url_element = etree.Element('url')
            url_element.text = url
            git_remote_config.append(url_element)
            remote_config.append(git_remote_config)
            scm.append(remote_config)

            branches = etree.Element('branches')
            branch_spec = etree.Element('hudson.plugins.git.BranchSpec')
            branch_spec_name = etree.Element('name')
            branch_spec_name.text = '*/master'
            branch_spec.append(branch_spec_name)
            branches.append(branch_spec)
            scm.append(branches)

            generate_submodule_configs = etree.Element('doGenerateSubmoduleConfigurations')
            generate_submodule_configs.text = 'false'
            scm.append(generate_submodule_configs)

            submodule_configs = etree.Element('submoduleCfg')
            submodule_configs.set('class', 'list')
            scm.append(submodule_configs)

            scm.append(etree.Element('extensions'))
        elif repo_type is 'svn':
            scm.set('class', 'hudson.scm.SubversionSCM')
            scm.set('plugin', 'subversion@2.4.5')

            locations = etree.Element('locations')

            module_location = etree.Element('hudson.scm.SubversionSCM_-ModuleLocation')

            remote = etree.Element('remote')
            remote.text = url
            module_location.append(remote)

            module_location.append(etree.Element('credentialsId'))

            local = etree.Element('local')
            local.text = '.'
            module_location.append(local)

            depth = etree.Element('depthOption')
            depth.text = 'infinity'
            module_location.append(depth)

            ignore_externals = etree.Element('ignoreExternalsOption')
            ignore_externals.text = 'true'
            module_location.append(ignore_externals)

            locations.append(module_location)

            scm.append(locations)

            scm.append(etree.Element('excludedRegions'))
            scm.append(etree.Element('includedRegions'))
            scm.append(etree.Element('excludedUsers'))
            scm.append(etree.Element('excludedRevprop'))
            scm.append(etree.Element('excludedCommitMessages'))

            updater = etree.Element('workspaceUpdater')
            updater.set('class', 'hudson.scm.subversion.UpdateUpdater')
            scm.append(updater)

            ignore_changes = etree.Element('ignoreDirPropChanges')
            ignore_changes.text = 'false'
            scm.append(ignore_changes)

            filter_changes = etree.Element('filterChangelog')
            filter_changes.text = 'false'
            scm.append(filter_changes)
        else:
            scm.set('class', 'hudson.scm.NullSCM')

        root.append(scm)

        roam = etree.Element('canRoam')
        roam.text = 'true'
        root.append(roam)

        disabled = etree.Element('disabled')
        disabled.text = 'false'
        root.append(disabled)

        upstream = etree.Element('blockBuildWhenDownstreamBuilding')
        upstream.text = 'false'
        root.append(upstream)

        downstream = etree.Element('blockBuildWhenUpstreamBuilding')
        downstream.text = 'false'
        root.append(downstream)

        root.append(etree.Element('triggers'))

        concurrent = etree.Element('concurrentBuild')
        concurrent.text = 'false'
        root.append(concurrent)

        root.append(etree.Element('builders'))
        root.append(etree.Element('publishers'))
        root.append(etree.Element('buildWrappers'))
        mine_serialized = etree.tostring(root, encoding='unicode', pretty_print=True)

        return mine_serialized
