import asyncio
from httpx import Response, RequestError


class RequestWrapper:
    def __init__(self, client):
        self._client = client
        self._backoff_factor = 0.5
        self._max_retries = 3

    async def request(self, method, url, **kwargs) -> Response:
        number_of_retries = 0

        while number_of_retries < self._max_retries:
            try:
                response = await self._client.request(method, url, **kwargs)

                if not self._needs_retry(response):
                    return response
            except RequestError as e:
                if number_of_retries == self._max_retries - 1:
                    raise e
            else:
                pass

            number_of_retries += 1
            backoff_time = self.get_backoff_time(number_of_retries)
            await asyncio.sleep(backoff_time)

        raise RuntimeError("Max retries exceeded.")

    def _needs_retry(self, response: Response) -> bool:
        return response.status_code >= 500

    def get_backoff_time(self, number_of_retries: int) -> float:
        return self._backoff_factor * (2 ** (number_of_retries - 1))