from lxml.etree import Element

from jenkins_job_manager.project_builder import ProjectBuilder


class WorkflowProjectBuilder(ProjectBuilder):
    PROJECT_DOMAIN = [
        'org',
        'jenkinsci',
        'plugins',
        'workflow',
        'multibranch',
        'WorkflowMultiBranchProject'
    ]

    def __init__(self):
        super().__init__()
        self.domain = self.join(self.PROJECT_DOMAIN)

    @staticmethod
    def join(elements: list) -> str:
        return '.'.join(elements)

    def append_description(self, parent: Element) -> None:
        description = Element('description')

        if self.description != '':
            description.text = self.description

        parent.append(description)

    @staticmethod
    def append_folder_views(parent: Element, owner: Element) -> None:
        folder_views = Element('folderViews')
        folder_views.set('class', 'jenkins.branch.MultiBranchProjectViewHolder')
        folder_views.set('plugin', 'branch-api@2.1.2')
        folder_views.append(owner)
        parent.append(folder_views)

    def append_health_metrics(self, parent: Element) -> None:
        health_metrics = Element('healthMetrics')
        worst_child_health_metric = Element(
            self.join(
                [
                    'com',
                    'cloudbees',
                    'hudson',
                    'plugins',
                    'folder',
                    'health',
                    'WorstChildHealthMetric'
                ]
            )
        )
        non_recursive = Element('nonRecursive')
        non_recursive.text = 'false'
        worst_child_health_metric.append(non_recursive)
        health_metrics.append(worst_child_health_metric)
        parent.append(health_metrics)

    @staticmethod
    def append_icon(parent: Element, owner: Element) -> None:
        icon = Element('icon')
        icon.set('class', 'jenkins.branch.MetadataActionFolderIcon')
        icon.set('plugin', 'branch-api@2.1.2')
        icon.append(owner)
        parent.append(icon)

    @staticmethod
    def append_orphaned_item_strategy(parent: Element) -> None:
        orphaned_item_strategy = Element('orphanedItemStrategy')
        prune_dead_branches = Element('pruneDeadBranches')
        prune_dead_branches.text = 'true'
        orphaned_item_strategy.append(prune_dead_branches)
        days_to_keep = Element('daysToKeep')
        days_to_keep.text = '-1'
        orphaned_item_strategy.append(days_to_keep)
        number_to_keep = Element('numToKeep')
        number_to_keep.text = '-1'
        orphaned_item_strategy.append(number_to_keep)
        parent.append(orphaned_item_strategy)

    def append_disabled(
            self,
            parent: Element,
    ) -> None:
        disabled = Element('disabled')

        if self.enabled:
            disabled.text = 'false'
        else:
            disabled.text = 'true'

        parent.append(disabled)

    def append_sources(
            self,
            parent: Element,
            owner: Element,
    ) -> None:
        sources = Element('sources')
        data = Element('data')
        branch_source = Element('jenkins.branch.BranchSource')
        source = Element('source')
        source.set('class', 'jenkins.plugins.git.GitSCMSource')
        source.set('plugin', 'git@3.9.3')
        identifier = Element('id')
        # identifier.text = 'Not sure what to put here yet. A UUID?'
        source.append(identifier)
        remote = Element('remote')
        remote.text = self.repository_locator
        credentials_identifier = Element('credentialsId')
        source.append(credentials_identifier)
        traits = Element('traits')
        branch_discovery_trait = Element(
            'jenkins.plugins.git.traits.BranchDiscoveryTrait'
        )
        traits.append(branch_discovery_trait)
        source.append(traits)
        strategy = Element('strategy')
        strategy.set('class', 'jenkins.branch.DefaultBranchPropertyStrategy')
        properties = Element('properties')
        properties.set('class', 'empty-list')
        strategy.append(properties)
        data.append(branch_source)
        sources.append(data)
        sources.append(owner)

        parent.append(sources)

    def build(self) -> Element:
        project = Element(self.domain)

        project.append(Element('actions'))
        self.append_description(project)
        project.append(Element('properties'))

        owner = Element('owner')
        owner.set('class', self.domain)
        owner.set('reference', '../..')

        self.append_folder_views(project, owner)
        self.append_health_metrics(project)
        self.append_icon(project, owner)
        self.append_orphaned_item_strategy(project)
        project.append(Element('triggers'))
        self.append_disabled(project)
        self.append_sources(project, owner)

        return project
