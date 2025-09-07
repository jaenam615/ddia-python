from chatper_10.pipeline.repository import PipelineRepository
from chatper_10.pipeline.transformer import PipelineTransformer


class PipelineProcessor:
    def __init__(self, repository: PipelineRepository, transformer: PipelineTransformer):
        self._repository = repository
        self._transformer = transformer

    async def process(self) -> list[dict]:

        return await  self._repository.get_data()

    async def transform(self, data: list[dict]):
        return await self._transformer.transform(data)