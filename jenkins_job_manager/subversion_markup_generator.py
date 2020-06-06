from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class SubversionMarkupGenerator:
    @staticmethod
    def append_subversion(element: Element, locator: str) -> None:
        element.append(
            SubversionMarkupGenerator._generate_locations(locator)
        )
        element.append(Element('excludedRegions'))
        element.append(Element('includedRegions'))
        element.append(Element('excludedUsers'))
        element.append(Element('excludedRevprop'))
        element.append(Element('excludedCommitMessages'))
        element.append(SubversionMarkupGenerator._generate_updater())
        element.append(
            Helper.create_false_boolean_element(tag='ignoreDirPropChanges')
        )
        element.append(
            Helper.create_false_boolean_element(tag='filterChangelog')
        )

    @staticmethod
    def _generate_locations(locator: str) -> Element:
        locations = Element('locations')
        module_location = Element(
            'hudson.scm.SubversionSCM_-ModuleLocation'
        )
        module_location.append(
            Helper.create_element_with_text(
                tag='remote',
                text=locator,
            )
        )
        module_location.append(Element('credentialsId'))
        module_location.append(
            Helper.create_element_with_text(
                tag='local',
                text='.',
            )
        )
        module_location.append(
            Helper.create_element_with_text(
                tag='depthOption',
                text='infinity',
            )
        )
        module_location.append(
            Helper.create_true_boolean_element('ignoreExternalsOption')
        )
        locations.append(module_location)

        return locations

    @staticmethod
    def _generate_updater() -> Element:
        updater = Element('workspaceUpdater')
        updater.set('class', 'hudson.scm.subversion.UpdateUpdater')

        return updater
