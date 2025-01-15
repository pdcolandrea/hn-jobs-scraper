import asyncio
import json
import pandas as pd
from pydantic import BaseModel
from typing import Optional

from extract import HackerNewsJobExtractor
from parse import HNJobParser


async def main():
    extractor = HackerNewsJobExtractor()
    extraction_result = await extractor.start()

    parser = HNJobParser(extraction_result)
    results = parser.start()

    # Debugging: Print the first few results to check structure
    print("Sample results:", results[:3])  # Adjust the slice as needed

    # Convert results to DataFrame
    df = pd.DataFrame(results)
    
    # Check if DataFrame is empty or has missing columns
    if df.empty:
        print("No data to save. Please check the extraction and parsing logic.")
    else:
        # Save as Excel file
        df.to_excel('output/hn_jobs.xlsx', index=False)
        
        # Optionally also save as CSV
        df.to_csv('output/hn_jobs.csv', index=False)
        
        print(f"Saved {len(results)} jobs to output/hn_jobs.xlsx and output/hn_jobs.csv")


if __name__ == "__main__":
    asyncio.run(main())
