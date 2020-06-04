from lxml.etree import Element

from jenkins_job_manager.git_markup_generator import GitMarkupGenerator
from jenkins_job_manager.subversion_markup_generator import \
    SubversionMarkupGenerator
from jenkins_job_manager.version_control_constants import \
    VersionControlConstants


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
    def generate_scm_for_repository_type(
            locator: str,
            repository_type: str
    ) -> Element:
        scm = Element('scm')

        if repository_type == VersionControlConstants.GIT_TYPE:
            scm.set('class', 'hudson.plugins.git.GitSCM')
            scm.set('plugin', 'git@4.2.2')
            git_generator = GitMarkupGenerator()
            scm.append(git_generator.generate_version())
            scm.append(git_generator.generate_remote_configuration(locator))
            scm.append(git_generator.generate_branches())
            scm.append(git_generator.generate_do_submodules())
            scm.append(git_generator.generate_submodule_configs())
            scm.append(Element('extensions'))
        elif repository_type == VersionControlConstants.SUBVERSION_TYPE:
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
