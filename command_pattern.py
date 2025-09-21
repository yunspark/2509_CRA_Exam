from abc import ABC, abstractmethod

class TV:
    def turn_on(self):
        print('Turn on')
        ...

class Command(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("execute method is not implemented")

class TVonCommand(Command):
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self):
        self.tv.turn_on()

class Invoker:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def run(self):
        self.command.execute()

tv = TV()
tv_cmd = TVonCommand(tv)

remote_ctrl = Invoker()
remote_ctrl.set_command(tv_cmd)
remote_ctrl.run()

