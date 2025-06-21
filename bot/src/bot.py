from navigator import Navigator

class Bot:
    def __init__(self) -> None:
        self.navigator = Navigator()

        self.do_shutdown = False

    def run(self):
        """
        Bots when ran, start and wait for input.
        On input, they enter a command, and execute that command
        """

        while True:
            # Stop if the bot has had a shutdown command
            if self.do_shutdown:
                break

            command, params = self.listen_for_command() # type: ignore

            raise NotImplementedError

    def listen_for_command(self) -> tuple[function, list[str]]: # type: ignore
        raise NotImplementedError