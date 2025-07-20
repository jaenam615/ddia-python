from abc import abstractmethod, ABCMeta


class ClientInterface(metaclass=ABCMeta):
    @abstractmethod
    def connect(self):
        """
        connects to a database and returns a connection
        """

    @abstractmethod
    def close(self):
        """
        closes a connection
        """