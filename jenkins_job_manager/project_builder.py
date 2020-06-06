from lxml.etree import Element

from jenkins_job_manager.repository_settings import RepositorySettings


class ProjectBuilder:
    @property
    def repository_settings(self) -> RepositorySettings:
        return self._repository_settings

    @repository_settings.getter
    def repository_settings(self) -> RepositorySettings:
        return self._repository_settings

    @repository_settings.setter
    def repository_settings(self, value: RepositorySettings) -> None:
        self._repository_settings = value

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
        self.repository_settings = None
        self.description = ''
        self.enabled = True

    def build(self) -> Element:
        pass
