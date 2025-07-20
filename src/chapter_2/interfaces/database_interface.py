from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def create_user(self):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_one_user(self, user_id: str):
        pass