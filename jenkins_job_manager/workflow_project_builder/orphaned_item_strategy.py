from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class OrphanedItemStrategy:
    @staticmethod
    def append_orphaned_item_strategy(parent: Element) -> None:
        orphaned_item_strategy = Element('orphanedItemStrategy')
        orphaned_item_strategy.set(
            'class',
            Helper.join(
                Helper.folder_domain + [
                    'computed',
                    'DefaultOrphanedItemStrategy'
                ]
            )
        )
        orphaned_item_strategy.set('plugin', 'cloudbees-folder@6.7')
        orphaned_item_strategy.append(
            Helper.create_true_boolean_element(tag='pruneDeadBranches')
        )
        orphaned_item_strategy.append(
            Helper.create_element_with_integer(
                tag='daysToKeep',
                integer=-1,
            )
        )
        orphaned_item_strategy.append(
            Helper.create_element_with_integer(
                tag='numToKeep',
                integer=-1,
            )
        )
        parent.append(orphaned_item_strategy)
