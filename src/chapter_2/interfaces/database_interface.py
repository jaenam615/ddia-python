from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def create_resume(self):
        """
        Creates a resume in the database.
        :return:
        """
        pass

    @abstractmethod
    def get_resume(self, resume_id: int) -> dict | None:
        """
        Retrieves a resume by its ID.
        :param resume_id:
        :return : A dictionary representing the resume, or None if not found.
        """
        pass

    @abstractmethod
    def clean_up(self):
        """
        Cleans up the database by removing all resumes.
        """
        pass
