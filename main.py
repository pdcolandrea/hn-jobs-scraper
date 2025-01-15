import asyncio
import json
from pydantic import BaseModel
from typing import Optional

from extract import HackerNewsJobExtractor
from parse import HNJobParser

async def main():
    extractor = HackerNewsJobExtractor()
    extraction_result = await extractor.start()

    # parser = HNJobParser(extraction_result)
    # parser.start()


if __name__ == "__main__":
    asyncio.run(main())
