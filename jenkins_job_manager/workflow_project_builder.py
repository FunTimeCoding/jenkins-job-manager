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
        self.domain = WorkflowProjectBuilder.join(self.PROJECT_DOMAIN)

    @staticmethod
    def join(elements: list) -> str:
        return '.'.join(elements)

    def append_description(self, parent: Element) -> None:
        description = Element('description')

        if self.description != '':
            description.text = self.description

        parent.append(description)

    def create_owner(self) -> Element:
        owner = Element('owner')
        owner.set('class', self.domain)
        owner.set('reference', '../..')

        return owner

    def append_folder_views(self, parent: Element) -> None:
        folder_views = Element('folderViews')
        folder_views.set('class', 'jenkins.branch.MultiBranchProjectViewHolder')
        folder_views.set('plugin', 'branch-api@2.1.2')
        folder_views.append(self.create_owner())
        parent.append(folder_views)

    @staticmethod
    def append_health_metrics(parent: Element) -> None:
        health_metrics = Element('healthMetrics')
        worst_child_health_metric = Element(
            WorkflowProjectBuilder.join(
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
        worst_child_health_metric.set('plugin', 'cloudbees-folder@6.7')
        non_recursive = Element('nonRecursive')
        non_recursive.text = 'false'
        worst_child_health_metric.append(non_recursive)
        health_metrics.append(worst_child_health_metric)
        parent.append(health_metrics)

    def append_icon(self, parent: Element) -> None:
        icon = Element('icon')
        icon.set('class', 'jenkins.branch.MetadataActionFolderIcon')
        icon.set('plugin', 'branch-api@2.1.2')
        icon.append(self.create_owner())
        parent.append(icon)

    @staticmethod
    def append_orphaned_item_strategy(parent: Element) -> None:
        orphaned_item_strategy = Element('orphanedItemStrategy')
        orphaned_item_strategy.set(
            'class',
            WorkflowProjectBuilder.join(
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
    ) -> None:
        sources = Element('sources')
        sources.set(
            'class',
            'jenkins.branch.MultiBranchProject$BranchSourceList'
        )
        sources.set('plugin', 'branch-api@2.1.2')
        data = Element('data')
        branch_source = Element('jenkins.branch.BranchSource')
        source = Element('source')
        source.set('class', 'jenkins.plugins.git.GitSCMSource')
        source.set('plugin', 'git@3.9.3')
        identifier = Element('id')
        # Not sure what to put here yet. A UUID?
        identifier.text = 'example'
        source.append(identifier)
        remote = Element('remote')
        remote.text = self.repository_locator
        source.append(remote)
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
        branch_source.append(source)
        branch_source.append(strategy)
        data.append(branch_source)
        sources.append(data)
        sources.append(self.create_owner())

        parent.append(sources)

    def append_factory(
            self,
            parent: Element,
    ) -> None:
        factory = Element('factory')
        factory.set(
            'class',
            WorkflowProjectBuilder.join(
                [
                    'org',
                    'jenkinsci',
                    'plugins',
                    'workflow',
                    'multibranch',
                    'WorkflowBranchProjectFactory'
                ]
            )
        )
        factory.append(self.create_owner())
        script_path = Element('scriptPath')
        script_path.text = 'Jenkinsfile'
        factory.append(script_path)
        parent.append(factory)

    def build(self) -> Element:
        project = Element(self.domain)
        project.set('plugin', 'workflow-multibranch@2.20')

        project.append(Element('actions'))
        self.append_description(project)
        project.append(Element('properties'))

        self.append_folder_views(project)
        self.append_health_metrics(project)
        self.append_icon(project)
        self.append_orphaned_item_strategy(project)
        project.append(Element('triggers'))
        self.append_disabled(project)
        self.append_sources(project)
        self.append_factory(project)

        return project
