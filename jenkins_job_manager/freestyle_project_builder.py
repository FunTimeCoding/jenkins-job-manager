from lxml.etree import Element

from jenkins_job_manager.general_markup_generator import GeneralMarkupGenerator
from jenkins_job_manager.project_builder import ProjectBuilder
from jenkins_job_manager.publisher_markup_generator import \
    PublisherMarkupGenerator


class FreestyleProjectBuilder(ProjectBuilder):
    @property
    def repository_type(self) -> str:
        return ''

    @property
    def labels(self) -> str:
        return ''

    @property
    def build_command(self) -> str:
        return ''

    @property
    def junit(self) -> str:
        return ''

    @property
    def checkstyle(self) -> str:
        return ''

    @property
    def hypertext_report(self) -> str:
        return ''

    @property
    def recipients(self) -> str:
        return ''

    @repository_type.setter
    def repository_type(self, value: str) -> None:
        self._repository_type = value

    @labels.setter
    def labels(self, value: str) -> None:
        self._labels = value

    @build_command.setter
    def build_command(self, value: str) -> None:
        self._build_command = value

    @junit.setter
    def junit(self, value: str) -> None:
        self._junit = value

    @checkstyle.setter
    def checkstyle(self, value: str) -> None:
        self._checkstyle = value

    @hypertext_report.setter
    def hypertext_report(self, value: str) -> None:
        self._hypertext_report = value

    @recipients.setter
    def recipients(self, value: str) -> None:
        self._recipients = value

    def __init__(self):
        super().__init__()
        self.repository_type = ''
        self.labels = ''
        self.build_command = ''
        self.junit = ''
        self.checkstyle = ''
        self.hypertext_report = ''
        self.recipients = ''

    def build(self) -> Element:
        project = Element('project')
        project.append(Element('actions'))
        description = Element('description')

        if self.description != '':
            description.text = self.description

        project.append(description)
        generator = GeneralMarkupGenerator()
        project.append(generator.generate_dependencies())
        project.append(Element('properties'))
        scm = generator.generate_scm_for_repository_type(
            locator=self.repository_locator,
            repository_type=self.repository_type
        )
        project.append(scm)

        if self.labels == '':
            project.append(generator.generate_roam(True))
        else:
            project.append(generator.generate_assigned_node(self.labels))
            project.append(generator.generate_roam(False))

        project.append(generator.generate_disabled())
        project.append(generator.generate_upstream())
        project.append(generator.generate_downstream())
        triggers = Element('triggers')

        if self.build_command != '':
            timer_trigger = Element('hudson.triggers.TimerTrigger')
            timer_spec = Element('spec')
            # End of week build.
            timer_spec.text = 'H 6 * * 5'
            # End of day build.
            # timer_spec.text = 'H 6 * * 1-5'
            timer_trigger.append(timer_spec)
            triggers.append(timer_trigger)
            scm_trigger = Element('hudson.triggers.SCMTrigger')
            scm_spec = Element('spec')
            scm_spec.text = 'H/30 * * * *'
            scm_trigger.append(scm_spec)
            hooks = Element('ignorePostCommitHooks')
            hooks.text = 'false'
            scm_trigger.append(hooks)
            triggers.append(scm_trigger)

        project.append(triggers)
        project.append(generator.generate_concurrent())
        builders = Element('builders')

        if self.build_command != '':
            shell = Element('hudson.tasks.Shell')
            command = Element('command')
            command.text = self.build_command
            shell.append(command)
            builders.append(shell)

        project.append(builders)
        publishers = Element('publishers')

        if self.junit != '':
            junit = Element('hudson.tasks.junit.JUnitResultArchiver')
            junit.set('plugin', 'junit@1.24')
            results = Element('testResults')
            results.text = self.junit
            junit.append(results)
            keep_long_output = Element('keepLongStdio')
            keep_long_output.text = 'false'
            junit.append(keep_long_output)
            health_factor = Element('healthScaleFactor')
            health_factor.text = '1.0'
            junit.append(health_factor)
            allow_empty = Element('allowEmptyResults')
            allow_empty.text = 'false'
            junit.append(allow_empty)
            publishers.append(junit)

        if self.checkstyle != '':
            checkstyle = Element(
                'hudson.plugins.checkstyle.CheckStylePublisher'
            )
            checkstyle.set('plugin', 'checkstyle@3.50')
            checkstyle.append(Element('healthy'))
            checkstyle.append(Element('unHealthy'))
            threshold = Element('thresholdLimit')
            threshold.text = 'low'
            checkstyle.append(threshold)
            name = Element('pluginName')
            # This space belongs here.
            name.text = '[CHECKSTYLE] '
            checkstyle.append(name)
            checkstyle.append(Element('defaultEncoding'))
            run_on_failed = Element('canRunOnFailed')
            run_on_failed.text = 'true'
            checkstyle.append(run_on_failed)
            previous_build_reference = Element('usePreviousBuildAsReference')
            previous_build_reference.text = 'false'
            checkstyle.append(previous_build_reference)
            stable_build_reference = Element('useStableBuildAsReference')
            stable_build_reference.text = 'false'
            checkstyle.append(stable_build_reference)
            delta_values = Element('useDeltaValues')
            delta_values.text = 'false'
            checkstyle.append(delta_values)
            thresholds = Element('thresholds')
            thresholds.set('plugin', 'analysis-core@1.95')
            unstable_total_all = Element('unstableTotalAll')
            thresholds.append(unstable_total_all)
            unstable_total_high = Element('unstableTotalHigh')
            thresholds.append(unstable_total_high)
            unstable_total_normal = Element('unstableTotalNormal')
            thresholds.append(unstable_total_normal)
            unstable_total_low = Element('unstableTotalLow')
            thresholds.append(unstable_total_low)
            unstable_new_all = Element('unstableNewAll')
            thresholds.append(unstable_new_all)
            unstable_new_high = Element('unstableNewHigh')
            thresholds.append(unstable_new_high)
            unstable_new_normal = Element('unstableNewNormal')
            thresholds.append(unstable_new_normal)
            unstable_new_low = Element('unstableNewLow')
            thresholds.append(unstable_new_low)
            failed_total_all = Element('failedTotalAll')
            thresholds.append(failed_total_all)
            failed_total_high = Element('failedTotalHigh')
            thresholds.append(failed_total_high)
            failed_total_normal = Element('failedTotalNormal')
            thresholds.append(failed_total_normal)
            failed_total_low = Element('failedTotalLow')
            thresholds.append(failed_total_low)
            failed_new_all = Element('failedNewAll')
            thresholds.append(failed_new_all)
            failed_new_high = Element('failedNewHigh')
            thresholds.append(failed_new_high)
            failed_new_normal = Element('failedNewNormal')
            thresholds.append(failed_new_normal)
            failed_new_low = Element('failedNewLow')
            thresholds.append(failed_new_low)
            checkstyle.append(thresholds)
            detect_modules = Element('shouldDetectModules')
            detect_modules.text = 'false'
            checkstyle.append(detect_modules)
            compute = Element('dontComputeNew')
            compute.text = 'true'
            checkstyle.append(compute)
            relative_paths = Element('doNotResolveRelativePaths')
            relative_paths.text = 'false'
            checkstyle.append(relative_paths)
            pattern = Element('pattern')
            pattern.text = self.checkstyle
            checkstyle.append(pattern)
            publishers.append(checkstyle)

        if self.hypertext_report != '':
            hypertext_report = PublisherMarkupGenerator.generate_hypertext(
                hypertext_report=self.hypertext_report
            )
            publishers.append(hypertext_report)

        mailer = Element(
            'hudson.tasks.Mailer'
        )
        mailer.set('plugin', 'mailer@1.21')
        recipients = Element('recipients')

        if self.recipients != '':
            recipients.text = self.recipients

        mailer.append(recipients)
        every_unstable_build = Element('dontNotifyEveryUnstableBuild')
        every_unstable_build.text = 'false'
        mailer.append(every_unstable_build)
        individuals = Element('sendToIndividuals')
        individuals.text = 'true'
        mailer.append(individuals)
        publishers.append(mailer)
        project.append(publishers)
        project.append(Element('buildWrappers'))

        return project
