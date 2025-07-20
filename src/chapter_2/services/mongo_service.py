from chapter_2.constants import DummyData
from chapter_2.interfaces.database_interface import DatabaseInterface

class MongoService(DatabaseInterface):
    def __init__(self, client):
        self._client = client.connect()
        self._db = self._client["testdb"]

    def create_resume(self):
        dummy = DummyData

        resume_doc = {
            "first_name": dummy.first_name,
            "last_name": dummy.last_name,
            "date_of_birth": dummy.date_of_birth,
            "work_experience": dummy.work_experiences,
            "education": dummy.education,
        }

        result = self._db.resumes.insert_one(resume_doc)
        return result.inserted_id

    def get_resume(self, resume_id: int) -> dict | None:
        from bson.objectid import ObjectId

        if isinstance(resume_id, str):
            try:
                resume_id = ObjectId(resume_id)
            except Exception:
                return None

        resume = self._db.resumes.find_one({"_id": resume_id})
        if not resume:
            return None

        resume_obj = {
            "id": 0,
            "first_name": resume.get("first_name"),
            "last_name": resume.get("last_name"),
            "date_of_birth": resume.get("date_of_birth"),
            "work_experiences": resume.get("work_experience", []),
            "education": resume.get("education", []),
        }
        return resume_obj

    def clean_up(self):
        self._db.resumes.delete_many({})

    def close(self):
        self._client.close()