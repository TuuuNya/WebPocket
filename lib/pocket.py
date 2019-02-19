from lib.cmd2 import Cmd


class Pocket(Cmd):
    prompt = "{}WebPocket{} > ".format("\033[4m", "\033[0m")

    def __init__(self):
        super().__init__()
        self.hidden_commands.extend(['alias', 'edit', 'macro', 'py', 'pyscript', 'shell', 'shortcuts', 'load'])

    def do_list(self, args):
        self.poutput("list all module")

    def do_set(self, args):
        pass
