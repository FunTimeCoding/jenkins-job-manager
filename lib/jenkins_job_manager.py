import argparse
from lxml import etree


class JenkinsJobManager:
    def run(self):
        parser = argparse.ArgumentParser(description='Generate a config.xml for jenkins jobs.')
        required_named = parser.add_argument_group('required named arguments')
        required_named.add_argument('-u', '--url', help='URL to the repository to check out on Jenkins')
        args = parser.parse_args()

        if args.url is not None:
            print('URL:', args.url)
            output = self.create_xml(url=args.url, repo_type="git")
            print(output)
        else:
            parser.print_help()

        return 0

    @staticmethod
    def create_xml(url, repo_type="git"):
        root = etree.Element("project")
        root.append(etree.Element("actions"))

        desc = etree.Element("description")
        root.append(desc)

        dependencies = etree.Element("keepDependencies")
        dependencies.text = "false"
        root.append(dependencies)

        properties = etree.Element("properties")

        # disk_usage = etree.Element("hudson.plugins.disk__usage.DiskUsageProperty")
        # disk_usage.set("plugin", "disk-usage@0.24")
        # properties.append(disk_usage)

        root.append(properties)

        scm = etree.Element("scm")
        if repo_type is "git":
            scm.set("class", "hudson.plugins.git.GitSCM")
            scm.set("plugin", "git@2.3.2")

            version = etree.Element("configVersion")
            version.text = "2"
            scm.append(version)

            remote_config = etree.Element("userRemoteConfigs")
            git_remote_config = etree.Element("hudson.plugins.git.UserRemoteConfig")
            url_element = etree.Element("url")
            url_element.text = url
            git_remote_config.append(url_element)
            remote_config.append(git_remote_config)
            scm.append(remote_config)

            branches = etree.Element("branches")
            branch_spec = etree.Element("hudson.plugins.git.BranchSpec")
            branch_spec_name = etree.Element("name")
            branch_spec_name.text = "*/master"
            branch_spec.append(branch_spec_name)
            branches.append(branch_spec)
            scm.append(branches)

            generate_submodule_configs = etree.Element("doGenerateSubmoduleConfigurations")
            generate_submodule_configs.text = "false"
            scm.append(generate_submodule_configs)

            submodule_configs = etree.Element("submoduleCfg")
            submodule_configs.set("class", "list")
            scm.append(submodule_configs)

            scm.append(etree.Element("extensions"))
        else:
            scm.set("class", "hudson.scm.NullSCM")

        root.append(scm)

        roam = etree.Element("canRoam")
        roam.text = "true"
        root.append(roam)

        disabled = etree.Element("disabled")
        disabled.text = "false"
        root.append(disabled)

        upstream = etree.Element("blockBuildWhenDownstreamBuilding")
        upstream.text = "false"
        root.append(upstream)

        downstream = etree.Element("blockBuildWhenUpstreamBuilding")
        downstream.text = "false"
        root.append(downstream)

        root.append(etree.Element("triggers"))

        concurrent = etree.Element("concurrentBuild")
        concurrent.text = "false"
        root.append(concurrent)

        root.append(etree.Element("builders"))
        root.append(etree.Element("publishers"))
        root.append(etree.Element("buildWrappers"))
        mine_serialized = etree.tostring(root, encoding='unicode', pretty_print=True)

        return mine_serialized
