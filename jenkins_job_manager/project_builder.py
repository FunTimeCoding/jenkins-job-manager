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

    @repository_locator.getter
    def repository_locator(self) -> str:
        return self._repository_locator

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.getter
    def description(self) -> str:
        return self._description

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    @enabled.getter
    def enabled(self) -> bool:
        return self._enabled

    def __init__(self):
        self.repository_locator = ''
        self.description = ''
        self.enabled = True

    def build(self) -> Element:
        pass
