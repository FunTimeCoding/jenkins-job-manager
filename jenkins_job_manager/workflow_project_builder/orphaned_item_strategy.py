from jenkins_job_manager.helper import Helper
from lxml.etree import Element


class OrphanedItemStrategy:
    @staticmethod
    def prune_dead_branches(prune: bool):
        prune_dead_branches = Element('pruneDeadBranches')

        if prune:
            prune_dead_branches.text = 'true'
        else:
            prune_dead_branches.text = 'false'

        return prune_dead_branches

    @staticmethod
    def create_days_to_keep(days: int):
        days_to_keep = Element('daysToKeep')
        days_to_keep.text = str(days)

        return days_to_keep

    @staticmethod
    def create_number_to_keep(number: int):
        number_to_keep = Element('numToKeep')
        number_to_keep.text = str(number)

        return number_to_keep

    @staticmethod
    def append_orphaned_item_strategy(parent: Element) -> None:
        orphaned_item_strategy = Element('orphanedItemStrategy')
        orphaned_item_strategy.set(
            'class',
            Helper.join(
                [
                    'com',
                    'cloudbees',
                    'hudson',
                    'plugins',
                    'folder',
                    'computed',
                    'DefaultOrphanedItemStrategy'
                ]
            )
        )
        orphaned_item_strategy.set('plugin', 'cloudbees-folder@6.7')
        orphaned_item_strategy.append(
            OrphanedItemStrategy.prune_dead_branches(True)
        )
        orphaned_item_strategy.append(
            OrphanedItemStrategy.create_days_to_keep(-1)
        )
        orphaned_item_strategy.append(
            OrphanedItemStrategy.create_number_to_keep(-1)
        )
        parent.append(orphaned_item_strategy)
