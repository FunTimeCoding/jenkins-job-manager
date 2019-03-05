from lxml.etree import Element


class ProjectBuilder:
    @property
    def repository_locator(self) -> str:
        return ''

    @property
    def description(self) -> str:
        return ''

    @property
    def enabled(self) -> bool:
        return True

    @repository_locator.setter
    def repository_locator(self, value: str) -> None:
        self._repository_locator = value

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    def __init__(self):
        self.repository_locator = ''
        self.description = ''
        self.enabled = True

    def build(self) -> Element:
        pass
