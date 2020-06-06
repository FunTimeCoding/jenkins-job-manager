from lxml.etree import Element

from jenkins_job_manager.git_markup_generator import GitMarkupGenerator
from jenkins_job_manager.subversion_markup_generator import \
    SubversionMarkupGenerator
from jenkins_job_manager.version_control_constants import \
    VersionControlConstants


class GeneralMarkupGenerator:
    @staticmethod
    def generate_scm_for_repository_type(
            locator: str,
            repository_type: str
    ) -> Element:
        scm = Element('scm')
        if repository_type == VersionControlConstants.GIT_TYPE:
            GeneralMarkupGenerator._append_git_scm(
                element=scm,
                locator=locator,
            )
        elif repository_type == VersionControlConstants.SUBVERSION_TYPE:
            GeneralMarkupGenerator._append_subversion_scm(
                element=scm,
                locator=locator,
            )
        else:
            scm.set('class', 'hudson.scm.NullSCM')

        return scm

    @staticmethod
    def _append_git_scm(element: Element, locator: str) -> None:
        element.set('class', 'hudson.plugins.git.GitSCM')
        element.set('plugin', 'git@4.2.2')
        element.set('class', 'hudson.plugins.git.GitSCM')
        GitMarkupGenerator.append_git(
            element=element,
            locator=locator,
        )
        element.append(Element('extensions'))

    @staticmethod
    def _append_subversion_scm(element: Element, locator: str) -> None:
        element.set('class', 'hudson.scm.SubversionSCM')
        element.set('plugin', 'subversion@2.4.5')
        element.set('class', 'hudson.scm.SubversionSCM')
        SubversionMarkupGenerator.append_subversion(
            element=element,
            locator=locator,
        )
