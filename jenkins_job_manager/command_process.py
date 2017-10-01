from subprocess import Popen, PIPE


class CommandProcess:
    def __init__(self, arguments: list) -> None:
        process = Popen(args=arguments, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        self.output = output.decode().strip()
        self.error = error.decode().strip()

    def print_output(self) -> None:
        if self.error != '':
            print(self.error)

        if self.output != '':
            print(self.output)
