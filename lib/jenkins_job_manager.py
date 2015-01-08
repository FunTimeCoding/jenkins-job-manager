import argparse
from lxml import etree


class JenkinsJobManager:
    def run(self):
        parser = argparse.ArgumentParser(description='Generate a config.xml for jenkins jobs.')
        requiredNamed = parser.add_argument_group('required named arguments')
        requiredNamed.add_argument('-u', '--url', help='URL to the repository to check out on Jenkins')
        args = parser.parse_args()

        if args.url is not None:
            print(args.url)
            self.create_xml()
        else:
            parser.print_help()

        return 0

    def create_xml(self):
        root = etree.Element("project")

        actions = etree.Element("actions")
        root.append(actions)

        desc = etree.Element("description")
        root.append(desc)

        root.append(etree.Element("keepDependencies"))
        root.append(etree.Element("properties"))
        root.append(etree.Element("scm"))
        root.append(etree.Element("canRoam"))
        root.append(etree.Element("disabled"))
        root.append(etree.Element("blockBuildWhenDownstreamBuilding"))
        root.append(etree.Element("blockBuildWhenUpstreamBuilding"))
        root.append(etree.Element("triggers"))
        root.append(etree.Element("concurrentBuild"))
        root.append(etree.Element("builders"))
        root.append(etree.Element("publishers"))
        root.append(etree.Element("buildWrappers"))
        print(etree.tostring(root, pretty_print=True).decode('utf-8'))
