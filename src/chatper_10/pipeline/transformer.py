import csv
from tempfile import NamedTemporaryFile
from pydantic import BaseModel
from typing import List


class UserTemplate(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: str
    website: str
    company: str


class PipelineTransformer:
    async def transform(self, data: List[dict]) -> str:
        with NamedTemporaryFile(mode="w+", encoding="utf-8", newline="", delete=False, suffix=".csv") as temp_file:
            fieldnames = list(UserTemplate.model_fields.keys())
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)

            writer.writeheader()

            for user in data:
                transformed_user = await self._transform_user(user)
                writer.writerow(transformed_user.dict())

            temp_file.flush()
            temp_file.seek(0)

        return temp_file.name

    async def _transform_user(self, user: dict) -> UserTemplate:
        return UserTemplate(
            id=user.get("id"),
            name=user.get("name"),
            username=user.get("name").lower().replace(" ", "_"),  # create a username
            email=user.get("email"),
            address=user.get("city", "N/A"),  # map city to address
            website="N/A",  # default
            company=user.get("role", "N/A")  # map role to company
        )