import pytest
from chapter_2.clients.mysql_client import MySQLClient
from chapter_2.constants import DummyData
from chapter_2.services.mysql_service import MySQLService

@pytest.fixture(scope="module")
def mysql_service():
    client = MySQLClient()
    service = MySQLService(client)
    service.clean_up()
    yield service
    service.clean_up()
    service.close()

def test_create_and_get_resume(mysql_service):
    resume_id = mysql_service.create_resume()
    assert resume_id is not None

    resume = mysql_service.get_resume(resume_id)
    assert resume is not None
    assert resume["first_name"] == DummyData.first_name
    assert len(resume["work_experiences"]) == len(DummyData.work_experiences)
    assert len(resume["education"]) == len(DummyData.education)

def test_get_resume_not_found(mysql_service):
    resume = mysql_service.get_resume(-1)
    assert resume is None