import csv

from chatper_10.pipeline.logic_container import PipelineLogicContainer

import asyncio

async def main():
    processor = PipelineLogicContainer().create_processor()

    data = await processor.process()
    transformed_data = await processor.transform(data)
    with open(transformed_data, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)

if __name__ == "__main__":
    asyncio.run(main())