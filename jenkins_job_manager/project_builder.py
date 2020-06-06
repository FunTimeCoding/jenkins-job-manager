from lxml.etree import Element


class ProjectBuilder:
    @property
    def repository_locator(self) -> str:
        return self._repository_locator

    @repository_locator.getter
    def repository_locator(self) -> str:
        return self._repository_locator

    @repository_locator.setter
    def repository_locator(self, value: str) -> None:
        self._repository_locator = value

    @property
    def description(self) -> str:
        return self._description

    @description.getter
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.getter
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    def __init__(self):
        self.repository_locator = ''
        self.description = ''
        self.enabled = True

    def build(self) -> Element:
        pass
