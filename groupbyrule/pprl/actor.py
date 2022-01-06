from abc import ABC, abstractmethod


class Actor(ABC):

    @abstractmethod
    def query(self, msg):
        pass

    @abstractmethod
    def send(self, actor, data, msg):
        pass


class Remote(Actor, ABC):

    def __init__(self, address):
        pass
