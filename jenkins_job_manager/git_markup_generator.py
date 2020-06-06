from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class GitMarkupGenerator:
    @staticmethod
    def append_git(element: Element, locator: str) -> None:
        element.append(
            Helper.create_element_with_integer(
                tag='configVersion',
                integer=2
            )
        )
        element.append(
            GitMarkupGenerator._generate_remote_configuration(locator)
        )
        element.append(GitMarkupGenerator._generate_branches())
        element.append(
            Helper.create_false_boolean_element(
                tag='doGenerateSubmoduleConfigurations',
            )
        )
        element.append(GitMarkupGenerator._generate_submodule_configs())

    @staticmethod
    def _generate_remote_configuration(locator: str) -> Element:
        configuration = Element('userRemoteConfigs')
        git_remote_configuration_tag = 'hudson.plugins.git.UserRemoteConfig'
        git_remote_configuration = Element(git_remote_configuration_tag)
        locator_element = Element('url')
        locator_element.text = locator
        git_remote_configuration.append(locator_element)
        configuration.append(git_remote_configuration)

        return configuration

    @staticmethod
    def _generate_branches() -> Element:
        branches = Element('branches')
        branch_specification = Element('hudson.plugins.git.BranchSpec')
        branch_specification_name = Element('name')
        branch_specification_name.text = '*/master'
        branch_specification.append(branch_specification_name)
        branches.append(branch_specification)

        return branches

    @staticmethod
    def _generate_submodule_configs() -> Element:
        submodule_configs = Element('submoduleCfg')
        submodule_configs.set('class', 'list')

        return submodule_configs
