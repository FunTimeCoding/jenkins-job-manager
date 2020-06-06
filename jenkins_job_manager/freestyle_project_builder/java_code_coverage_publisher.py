from lxml.etree import Element

from jenkins_job_manager.helper import Helper


class JavaCodeCoveragePublisher:
    @staticmethod
    def append_patterns(element: Element) -> None:
        element.append(
            Helper.create_element_with_text(
                tag='execPattern',
                text='**/**.exec',
            )
        )
        element.append(
            Helper.create_element_with_text(
                tag='classPattern',
                text='**/classes',
            )
        )
        element.append(
            Helper.create_element_with_text(
                tag='sourcePattern',
                text='**/src/main/java',
            )
        )
        element.append(
            Helper.create_element_with_text(
                tag='sourceInclusionPattern',
                text=','.join(
                    [
                        '**/*.java',
                        '**/*.groovy',
                        '**/*.kt',
                        '**/*.kts',
                    ]
                ),
            )
        )
        element.append(
            Helper.create_empty_text_element(
                tag='sourceExclusionPattern',
            )
        )
        element.append(
            Helper.create_empty_text_element(
                tag='inclusionPattern',
            )
        )
        element.append(
            Helper.create_empty_text_element(
                tag='exclusionPattern',
            )
        )

    @staticmethod
    def append_minimum_limits(element: Element) -> None:
        element.append(
            Helper.create_element_with_integer(
                tag='minimumInstructionCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='minimumBranchCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='minimumComplexityCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='minimumLineCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='minimumMethodCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='minimumClassCoverage',
                integer=0,
            )
        )

    @staticmethod
    def append_maximum_limits(element: Element) -> None:
        element.append(
            Helper.create_element_with_integer(
                tag='maximumInstructionCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='maximumBranchCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='maximumComplexityCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='maximumLineCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='maximumMethodCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='maximumClassCoverage',
                integer=0,
            )
        )

    @staticmethod
    def append_delta_limits(element: Element) -> None:
        element.append(
            Helper.create_element_with_integer(
                tag='deltaInstructionCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='deltaBranchCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='deltaComplexityCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='deltaLineCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='deltaMethodCoverage',
                integer=0,
            )
        )
        element.append(
            Helper.create_element_with_integer(
                tag='deltaClassCoverage',
                integer=0,
            )
        )

    @staticmethod
    def generate() -> Element:
        publisher = Helper.create_plugin_element(
            tag='hudson.plugins.jacoco.JacocoPublisher',
            plugin='jacoco',
            version='3.0.5',
        )
        JavaCodeCoveragePublisher.append_patterns(element=publisher)
        publisher.append(
            Helper.create_false_boolean_element(tag='skipCopyOfSrcFiles')
        )
        JavaCodeCoveragePublisher.append_minimum_limits(
            element=publisher
        )
        JavaCodeCoveragePublisher.append_maximum_limits(
            element=publisher
        )
        publisher.append(
            Helper.create_false_boolean_element(tag='changeBuildStatus')
        )
        publisher.append(
            Helper.create_false_boolean_element(tag='runAlways')
        )
        JavaCodeCoveragePublisher.append_delta_limits(
            element=publisher
        )
        publisher.append(
            Helper.create_false_boolean_element(tag='buildOverBuild')
        )

        return publisher
