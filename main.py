import asyncio
import json
from pydantic import BaseModel
from typing import Optional

from extract import start_extraction
from parse import HNJobParser

async def main():
    extraction_result = await start_extraction()

    parser = HNJobParser(extraction_result)
    # parser.start()


if __name__ == "__main__":
    asyncio.run(main())
