from lxml.etree import Element


class GitMarkupGenerator:
    @staticmethod
    def generate_remote_configuration(locator: str) -> Element:
        configuration = Element('userRemoteConfigs')
        git_remote_configuration_tag = 'hudson.plugins.git.UserRemoteConfig'
        git_remote_configuration = Element(git_remote_configuration_tag)
        locator_element = Element('url')
        locator_element.text = locator
        git_remote_configuration.append(locator_element)
        configuration.append(git_remote_configuration)

        return configuration

    @staticmethod
    def generate_branches() -> Element:
        branches = Element('branches')
        branch_specification = Element('hudson.plugins.git.BranchSpec')
        branch_specification_name = Element('name')
        branch_specification_name.text = '*/master'
        branch_specification.append(branch_specification_name)
        branches.append(branch_specification)

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
