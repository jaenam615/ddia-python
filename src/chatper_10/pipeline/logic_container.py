from httpx import AsyncClient

from chapter_1.request_wrapper import RequestWrapper
from chatper_10.pipeline.processor import PipelineProcessor
from chatper_10.pipeline.repository import PipelineRepository
from chatper_10.pipeline.transformer import PipelineTransformer


class PipelineLogicContainer:
    def create_processor(self):
        async_client = AsyncClient()

        return PipelineProcessor(
            repository=PipelineRepository(
                request_wrapper=RequestWrapper(
                    client=async_client
                )
            ),
            transformer=PipelineTransformer()
        )