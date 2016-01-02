from signal import SIGINT, SIGHUP, SIGTERM

from circuits.protocols.irc import QUIT
from circuits import handler, BaseComponent, Timer

from .pancakesbot import IRCBot
from .events import terminate


class Core(BaseComponent):

    channel = "core"

    def init(self, config):
        self.config = config
        self.bot = IRCBot(**self.config).register(self)

    @handler("signal", channels="*")
    def signal(self, signo, stack):
        if signo == SIGHUP:
            pass
        elif signo in (SIGINT, SIGTERM):
            self.fire(QUIT("Received SIGTERM, terminating..."), self.bot)
            self.fire(terminate(), self.bot)
            Timer(1, terminate()).register(self)

    @handler("terminate")
    def _on_terminate(self):
        raise SystemExit(0)
