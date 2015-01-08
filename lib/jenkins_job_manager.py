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
            self.create_xml()
        else:
            parser.print_help()

        return 0

    def create_xml(self):
        my_parser = etree.XMLParser(remove_blank_text=True)
        original = etree.parse('/Users/shiin/Code/Personal/jenkins-tools/bare-job.xml', parser=my_parser)
        original_serialized = etree.tostring(original, encoding='unicode', pretty_print=True)
        print(original_serialized)

        root = etree.Element("project")
        root.append(etree.Element("actions"))

        desc = etree.Element("description")
        root.append(desc)

        dependencies = etree.Element("keepDependencies")
        dependencies.text = "false"
        root.append(dependencies)

        root.append(etree.Element("properties"))

        scm = etree.Element("scm")
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
        print(mine_serialized)

        if original_serialized == mine_serialized:
            print('equal')
        else:
            print('not equal')
