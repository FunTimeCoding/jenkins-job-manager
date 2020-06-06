from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class JUnitResultArchiver:
    @staticmethod
    def generate(result_path: str) -> Element:
        archiver = Helper.create_plugin_element(
            tag='hudson.tasks.junit.JUnitResultArchiver',
            plugin='junit',
            version='1.29',
        )
        archiver.append(
            Helper.create_element_with_text(
                tag='testResults',
                text=result_path,
            )
        )
        archiver.append(
            Helper.create_false_boolean_element(tag='keepLongStdio')
        )
        archiver.append(
            Helper.create_element_with_text(
                tag='healthScaleFactor',
                text='1.0',
            )
        )
        archiver.append(
            Helper.create_false_boolean_element(tag='allowEmptyResults')
        )

        return archiver
