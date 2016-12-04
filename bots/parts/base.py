class BaseBot:

    def __init__(self, name, *args, **kwargs):
        self.name = name

    def start(self):
        raise NotImplementedError('implement in subclass')
