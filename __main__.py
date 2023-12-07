import asyncio
from modules.processor import Processor


async def main():
    processor = Processor()
    await processor.run()


if __name__ == "__main__":
    asyncio.run(main())
