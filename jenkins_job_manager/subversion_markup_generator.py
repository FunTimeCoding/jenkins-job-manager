from lxml.etree import Element


class SubversionMarkupGenerator:
    @staticmethod
    def generate_locations(locator: str) -> Element:
        locations = Element('locations')
        module_tag = 'hudson.scm.SubversionSCM_-ModuleLocation'
        module_location = Element(module_tag)
        remote = Element('remote')
        remote.text = locator
        module_location.append(remote)
        module_location.append(Element('credentialsId'))
        local = Element('local')
        local.text = '.'
        module_location.append(local)
        depth = Element('depthOption')
        depth.text = 'infinity'
        module_location.append(depth)
        ignore_externals = Element('ignoreExternalsOption')
        ignore_externals.text = 'true'
        module_location.append(ignore_externals)
        locations.append(module_location)

        return locations

    @staticmethod
    def generate_updater() -> Element:
        updater = Element('workspaceUpdater')
        updater.set('class', 'hudson.scm.subversion.UpdateUpdater')

        return updater

    @staticmethod
    def generate_ignore_changes() -> Element:
        ignore_changes = Element('ignoreDirPropChanges')
        ignore_changes.text = 'false'

        return ignore_changes

    @staticmethod
    def generate_filter_changes() -> Element:
        filter_changes = Element('filterChangelog')
        filter_changes.text = 'false'

        return filter_changes
