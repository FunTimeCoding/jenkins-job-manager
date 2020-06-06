from lxml.etree import Element


class Helper:
    folder_domain = [
        'com',
        'cloudbees',
        'hudson',
        'plugins',
        'folder',
    ]

    @staticmethod
    def join(elements: list) -> str:
        return '.'.join(elements)

    @staticmethod
    def create_empty_text_element(tag: str) -> Element:
        element = Element(tag)
        element.text = ''

        return element

    @staticmethod
    def create_element_with_text(tag: str, text: str) -> Element:
        element = Element(tag)
        element.text = text

        return element

    @staticmethod
    def create_element_with_integer(tag: str, integer: int) -> Element:
        element = Element(tag)
        element.text = str(integer)

        return element

    @staticmethod
    def _create_element_with_boolean(tag: str, boolean: bool) -> Element:
        element = Element(tag)

        if boolean:
            element.text = 'true'
        else:
            element.text = 'false'

        return element

    @staticmethod
    def create_false_boolean_element(tag: str) -> Element:
        return Helper._create_element_with_boolean(
            tag=tag,
            boolean=False,
        )

    @staticmethod
    def create_true_boolean_element(tag: str) -> Element:
        return Helper._create_element_with_boolean(
            tag=tag,
            boolean=True,
        )

    @staticmethod
    def create_plugin_element(tag: str, plugin: str, version: str) -> Element:
        element = Element(tag)
        element.set('plugin', plugin + '@' + version)

        return element

    @staticmethod
    def create_element_with_class(tag: str, class_attribute: str) -> Element:
        element = Element(tag)
        element.set('class', class_attribute)

        return element
