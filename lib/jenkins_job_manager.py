import argparse

class JenkinsJobManager:

    def run(self):
        parser = argparse.ArgumentParser(description='Generate a config.xml for jenkins jobs.')
        parser.add_argument('-u', '--url', help='URL to the repository to check out on Jenkins')
        args = parser.parse_args()

        if not args.url == None:
            print(args.url)
        else:
            parser.print_help()

        return 0
