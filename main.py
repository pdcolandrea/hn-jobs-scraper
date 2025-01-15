import asyncio
import json
from pydantic import BaseModel
from typing import Optional

from extract import start_extraction


async def main():
    extraction_result = await start_extraction()
    print(extraction_result)

if __name__ == "__main__":
    asyncio.run(main())
