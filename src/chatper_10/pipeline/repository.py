from chapter_1.request_wrapper import RequestWrapper


class PipelineRepository:
    def __init__(self, request_wrapper:RequestWrapper):
        self._request_wrapper = request_wrapper

    async def get_data(self) -> list[dict]:
        url = "http://localhost:8000/users/"

        users = await self._request_wrapper.request(method="GET", url=url)

        return users.json()