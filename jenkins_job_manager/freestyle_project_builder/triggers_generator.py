from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class TriggersGenerator:
    @staticmethod
    def generate(build_command: str) -> Element:
        triggers = Element('triggers')

        if build_command:
            TriggersGenerator._append_timer_trigger(element=triggers)
            TriggersGenerator._append_scm_trigger(element=triggers)

        return triggers

    @staticmethod
    def _append_timer_trigger(element: Element) -> None:
        timer_trigger = Element('hudson.triggers.TimerTrigger')
        timer_trigger.append(
            Helper.create_element_with_text(
                tag='spec',
                # end of week, Friday mornings
                text='H 6 * * 5',
                # end of day, mornings
                # text='H 6 * * 1-5',
            )
        )
        element.append(timer_trigger)

    @staticmethod
    def _append_scm_trigger(element: Element) -> None:
        scm_trigger = Element('hudson.triggers.SCMTrigger')
        scm_trigger.append(
            Helper.create_element_with_text(
                tag='spec',
                text='H/30 * * * *'
            )
        )
        scm_trigger.append(
            Helper.create_false_boolean_element(tag='ignorePostCommitHooks')
        )
        element.append(scm_trigger)
