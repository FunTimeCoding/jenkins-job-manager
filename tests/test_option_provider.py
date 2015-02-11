from lib.option_provider import OptionProvider


def test_repo_type_git():
    provider = OptionProvider()
    assert provider.guess_repo_type('https://github.com/FunTimeCoding/dotfiles.git') == 'git'


def test_repo_type_svn():
    provider = OptionProvider()
    assert provider.guess_repo_type('svn+ssh://svn.rz.adition/adition_v4/branches/release-v4.28') == 'svn'


def test_not_a_string():
    provider = OptionProvider()
    assert provider.guess_repo_type(1) == ''
