import httpx
import asyncio

from src.chapter_1.request_wrapper import RequestWrapper

if __name__ == '__main__':
    client = httpx.AsyncClient()

    wrapper = RequestWrapper(
        client=client
    )

    url = "https://test.com"
    # url = "https://api.github.com"

    asyncio.run(wrapper.request(method="GET", url=url))

