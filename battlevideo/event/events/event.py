import abc

class Event(metaclass=abc.ABCMeta):

    def __init__(self, message: str):
        self.message = message

    def __repr__(self):
        return self.message
