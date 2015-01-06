import argparse

class JenkinsJobManager:

    def run(self):
        parser = argparse.ArgumentParser(description='Generate a config.xml for jenkins jobs.')
        requiredNamed = parser.add_argument_group('required named arguments')
        requiredNamed.add_argument('-u', '--url', help='URL to the repository to check out on Jenkins')
        args = parser.parse_args()

        if args.url is not None:
            print(args.url)
        else:
            parser.print_help()

        return 0
