from jenkins_job_manager.version_control_constants import \
    VersionControlConstants


class RepositorySettings:
    @property
    def repository_type(self) -> str:
        return self._repository_type

    @repository_type.getter
    def repository_type(self) -> str:
        return self._repository_type

    @repository_type.setter
    def repository_type(self, value: str) -> None:
        self._repository_type = value

    @property
    def repository_locator(self) -> str:
        return self._repository_locator

    @repository_locator.getter
    def repository_locator(self) -> str:
        return self._repository_locator

    @repository_locator.setter
    def repository_locator(self, value: str) -> None:
        self._repository_locator = value

    def __init__(self, repository_type: str, repository_locator: str):
        self.repository_locator = repository_locator

        if self.is_valid_repository_type(repository_type) is False:
            repository_type = self.guess_repository_type(
                self.repository_locator
            )

        self.repository_type = repository_type

    @staticmethod
    def get_repository_types() -> list:
        return [
            VersionControlConstants.GIT_TYPE,
            VersionControlConstants.SUBVERSION_TYPE
        ]

    @staticmethod
    def is_valid_repository_type(repository_type: str) -> bool:
        return repository_type in RepositorySettings.get_repository_types()

    @staticmethod
    def guess_repository_type(locator: str) -> str:
        repository_type = ''

        for valid_type in RepositorySettings.get_repository_types():
            if valid_type in locator:
                repository_type = valid_type

                break

        return repository_type
