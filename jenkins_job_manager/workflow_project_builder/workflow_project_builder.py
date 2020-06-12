from lxml.etree import Element

from jenkins_job_manager.helper import Helper
from jenkins_job_manager.repository_settings import RepositorySettings
from jenkins_job_manager.workflow_project_builder.orphaned_item_strategy \
    import OrphanedItemStrategy
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
    BRANCH_PLUGIN = 'branch-api@2.1.2'

    def __init__(self, repository_settings: RepositorySettings):
        super().__init__()
        self.repository_settings = repository_settings
        self.domain = Helper.join(self.PROJECT_DOMAIN)

    @staticmethod
    def _append_description(parent: Element, description: str) -> None:
        description_element = Element('description')

        if description:
            description_element.text = description

        parent.append(description_element)

    def _create_owner(self) -> Element:
        owner = Element('owner')
        owner.set('class', self.domain)
        owner.set('reference', '../..')

        return owner

    def _append_folder_views(self, parent: Element) -> None:
        folder_views = Element('folderViews')
        folder_views.set(
            'class',
            'jenkins.branch.MultiBranchProjectViewHolder'
        )
        folder_views.set(
            'plugin',
            WorkflowProjectBuilder.BRANCH_PLUGIN
        )
        folder_views.append(self._create_owner())
        parent.append(folder_views)

    @staticmethod
    def _append_health_metrics(parent: Element) -> None:
        health_metrics = Element('healthMetrics')
        worst_child_health_metric = Element(
            Helper.join(
                Helper.folder_domain + [
                    'health',
                    'WorstChildHealthMetric',
                ]
            )
        )
        worst_child_health_metric.set('plugin', 'cloudbees-folder@6.7')
        non_recursive = Element('nonRecursive')
        non_recursive.text = 'false'
        worst_child_health_metric.append(non_recursive)
        health_metrics.append(worst_child_health_metric)
        parent.append(health_metrics)

    def _append_icon(self, parent: Element) -> None:
        icon = Element('icon')
        icon.set('class', 'jenkins.branch.MetadataActionFolderIcon')
        icon.set(
            'plugin',
            WorkflowProjectBuilder.BRANCH_PLUGIN
        )
        icon.append(self._create_owner())
        parent.append(icon)

    def _append_source(
            self,
            parent: Element,
    ) -> None:
        source = Helper.create_element_with_class(
            tag='source',
            class_attribute='jenkins.plugins.git.GitSCMSource',
        )
        source.set('plugin', 'git@3.9.3')
        source.append(
            Helper.create_element_with_text(
                tag='id',
                # TODO: Not sure what to put here yet. A UUID?
                text='example',
            )
        )
        source.append(
            Helper.create_element_with_text(
                tag='remote',
                text=self.repository_settings.repository_locator,
            )
        )
        source.append(Element('credentialsId'))
        traits = Element('traits')
        traits.append(
            Element('jenkins.plugins.git.traits.BranchDiscoveryTrait')
        )
        source.append(traits)
        parent.append(source)

    def _append_branch_source(
            self,
            parent: Element,
    ) -> None:
        branch_source = Element('jenkins.branch.BranchSource')
        self._append_source(parent=branch_source)
        strategy = Helper.create_element_with_class(
            tag='strategy',
            class_attribute='jenkins.branch.DefaultBranchPropertyStrategy',
        )
        strategy.append(
            Helper.create_element_with_class(
                tag='properties',
                class_attribute='empty-list',
            )
        )
        branch_source.append(strategy)
        parent.append(branch_source)

    def _append_data(
            self,
            parent: Element,
    ) -> None:
        data = Element('data')
        self._append_branch_source(parent=data)
        parent.append(data)

    def _append_sources(
            self,
            parent: Element,
    ) -> None:
        sources = Helper.create_element_with_class(
            tag='sources',
            class_attribute=Helper.join(
                [
                    'jenkins',
                    'branch',
                    'MultiBranchProject$BranchSourceList',
                ]
            ),
        )
        sources.set(
            'plugin',
            WorkflowProjectBuilder.BRANCH_PLUGIN
        )
        self._append_data(parent=sources)
        sources.append(self._create_owner())
        parent.append(sources)

    def _append_factory(
            self,
            parent: Element,
    ) -> None:
        factory = Helper.create_element_with_class(
            tag='factory',
            class_attribute=Helper.join(
                [
                    'org',
                    'jenkinsci',
                    'plugins',
                    'workflow',
                    'multibranch',
                    'WorkflowBranchProjectFactory'
                ]
            ),
        )
        factory.append(self._create_owner())
        factory.append(
            Helper.create_element_with_text(
                tag='scriptPath',
                text='Jenkinsfile',
            )
        )
        parent.append(factory)

    @staticmethod
    def create_project(domain: str, description: str) -> Element:
        project = Helper.create_plugin_element(
            tag=domain,
            plugin='workflow-multibranch',
            version='2.20'
        )
        project.append(Element('actions'))
        WorkflowProjectBuilder._append_description(
            parent=project,
            description=description,
        )
        project.append(Element('properties'))

        return project

    def build(self) -> Element:
        project = WorkflowProjectBuilder.create_project(
            domain=self.domain,
            description=self.description,
        )
        self._append_folder_views(project)
        self._append_health_metrics(project)
        self._append_icon(project)
        OrphanedItemStrategy.append_orphaned_item_strategy(project)
        project.append(Element('triggers'))
        project.append(Helper.create_false_boolean_element(tag='disabled'))
        self._append_sources(project)
        self._append_factory(project)

        return project
