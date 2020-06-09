class FreestyleSettings:
    @property
    def build_command(self) -> str:
        return self._build_command

    @build_command.getter
    def build_command(self) -> str:
        return self._build_command

    @build_command.setter
    def build_command(self, value: str) -> None:
        self._build_command = value

    @property
    def labels(self) -> str:
        return self._labels

    @labels.getter
    def labels(self) -> str:
        return self._labels

    @labels.setter
    def labels(self, value: str) -> None:
        self._labels = value

    def __init__(self, build_command: str, labels: str):
        super().__init__()
        self._build_command = build_command
        self._labels = labels
