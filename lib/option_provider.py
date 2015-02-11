import argparse


class OptionProvider:
    def get_options(self):
        return dict()

    def print_help(self):
        raise Exception('No help available.')

    @staticmethod
    def is_valid_repo_type(repo_type):
        is_valid = False

        if repo_type in RepositoryTypeProvider.get_valid_repo_types():
            is_valid = True

        return is_valid

    @staticmethod
    def guess_repo_type(url):
        repo_type = ''

        if type(url) == str:
            for valid_type in RepositoryTypeProvider.get_valid_repo_types():
                print('valid type:' + valid_type)
                if valid_type in url:
                    repo_type = valid_type
                    break

        return repo_type


class ArgParseOptionProvider(OptionProvider):
    def __init__(self):
        self.options = dict()
        self.parser = self.create_arg_parser()

        args = self.parser.parse_args()

        self.options['repo_type'] = args.type
        self.options['verbose'] = args.verbose
        self.options['url'] = args.url

        if self.is_valid_repo_type(self.options['repo_type']) is False:
            self.options['repo_type'] = self.guess_repo_type(self.options['url'])

    def get_options(self):
        return self.options

    @staticmethod
    def create_arg_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='Generate a config.xml for jenkins jobs.')
        required_named = parser.add_argument_group('required named arguments')

        required_named.add_argument(
            '-u',
            '--url',
            help='URL to the repository to check out on Jenkins',
            default=''
        )

        valid_types = RepositoryTypeProvider.get_valid_repo_types()

        parser.add_argument(
            '-t',
            '--type',
            help='Repository type. Supported: ' + ', '.join(valid_types),
            choices=valid_types,
            default=''
        )

        parser.add_argument(
            '-v',
            '--verbose',
            help='Turn on some verbose messages.',
            action='store_true'
        )
        return parser

    def print_help(self):
        self.parser.print_help()


class RepositoryTypeProvider():
    @staticmethod
    def get_valid_repo_types():
        return ['svn', 'git']
