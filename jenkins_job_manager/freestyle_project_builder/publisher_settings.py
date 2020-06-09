class PublisherSettings:
    @property
    def junit(self) -> str:
        return self._junit

    @junit.getter
    def junit(self) -> str:
        return self._junit

    @junit.setter
    def junit(self, value: str) -> None:
        self._junit = value

    @property
    def checkstyle(self) -> str:
        return self._checkstyle

    @checkstyle.getter
    def checkstyle(self) -> str:
        return self._checkstyle

    @checkstyle.setter
    def checkstyle(self, value: str) -> None:
        self._checkstyle = value

    @property
    def hypertext_report(self) -> str:
        return self._hypertext_report

    @hypertext_report.getter
    def hypertext_report(self) -> str:
        return self._hypertext_report

    @hypertext_report.setter
    def hypertext_report(self, value: str) -> None:
        self._hypertext_report = value

    @property
    def jacoco(self) -> bool:
        return self._jacoco

    @jacoco.getter
    def jacoco(self) -> bool:
        return self._jacoco

    @jacoco.setter
    def jacoco(self, value: bool) -> None:
        self._jacoco = value

    @property
    def recipients(self) -> str:
        return self._recipients

    @recipients.getter
    def recipients(self) -> str:
        return self._recipients

    @recipients.setter
    def recipients(self, value: str) -> None:
        self._recipients = value

    def __init__(self):
        super().__init__()
        self._junit = ''
        self._checkstyle = ''
        self._hypertext_report = ''
        self._recipients = ''
        self._jacoco = False
