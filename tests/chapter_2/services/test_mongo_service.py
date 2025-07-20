import pytest
from chapter_2.clients.mongo_client import MongoDBClient
from chapter_2.constants import DummyData
from chapter_2.services.mongo_service import MongoService

@pytest.fixture(scope="module")
def mongo_service():
    client = MongoDBClient()
    service = MongoService(client)
    service.clean_up()
    yield service
    service.clean_up()
    service.close()

def test_create_and_get_resume(mongo_service):
    inserted_id = mongo_service.create_resume()
    assert inserted_id is not None

    resume = mongo_service.get_resume(inserted_id)
    assert resume is not None
    assert resume["first_name"] == DummyData.first_name
    assert len(resume["work_experiences"]) == len(DummyData.work_experiences)
    assert len(resume["education"]) == len(DummyData.education)

def test_get_resume_not_found(mongo_service):
    resume = mongo_service.get_resume("000000000000000000000000")
    assert resume is None