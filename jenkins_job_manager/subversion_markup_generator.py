from lxml.etree import Element


class SubversionMarkupGenerator:
    @staticmethod
    def create_remote(locator: str):
        remote = Element('remote')
        remote.text = locator

        return remote

    @staticmethod
    def create_local():
        local = Element('local')
        local.text = '.'

        return local

    @staticmethod
    def create_depth_option(depth: str):
        depth_option = Element('depthOption')
        depth_option.text = depth

        return depth_option

    @staticmethod
    def create_ignore_externals(ignore: bool):
        ignore_externals = Element('ignoreExternalsOption')

        if ignore:
            ignore_externals.text = 'true'
        else:
            ignore_externals.text = 'false'

        return ignore_externals

    @staticmethod
    def generate_locations(locator: str) -> Element:
        locations = Element('locations')
        module_location = Element(
            'hudson.scm.SubversionSCM_-ModuleLocation'
        )
        module_location.append(
            SubversionMarkupGenerator.create_remote(locator=locator)
        )
        module_location.append(Element('credentialsId'))
        module_location.append(
            SubversionMarkupGenerator.create_local()
        )
        module_location.append(
            SubversionMarkupGenerator.create_depth_option('infinity')
        )
        module_location.append(
            SubversionMarkupGenerator.create_ignore_externals(True)
        )
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
