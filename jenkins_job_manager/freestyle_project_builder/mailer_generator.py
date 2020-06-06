from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class MailerGenerator:
    @staticmethod
    def generate(recipients: str) -> Element:
        mailer = Helper.create_plugin_element(
            tag='hudson.tasks.Mailer',
            plugin='mailer',
            version='1.32',
        )
        recipients_element = Element('recipients')

        if recipients:
            recipients_element.text = recipients

        mailer.append(recipients_element)
        mailer.append(
            Helper.create_false_boolean_element(
                tag='dontNotifyEveryUnstableBuild',
            )
        )
        mailer.append(
            Helper.create_true_boolean_element(tag='sendToIndividuals')
        )

        return mailer
