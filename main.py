import asyncio
import json
import pandas as pd
from pydantic import BaseModel
from typing import Optional

from extract import HackerNewsJobExtractor
from parse import HNJobParser
from files import FileHelper


async def main():
    # De-duplicate listings
    file_helper = FileHelper()
    previous_listings = file_helper.open_last_output_file()

    # Create a set to store company names
    existing_company_names = set()

    # Loop through previous listings and add company names to set
    if isinstance(previous_listings, pd.DataFrame) and not previous_listings.empty:
        for _, row in previous_listings.iterrows():
            if "company_name" in row:
                existing_company_names.add(row["company_name"])

    print(f"Found {len(existing_company_names)} unique companies in previous listings")

    extractor = HackerNewsJobExtractor()
    extraction_result = await extractor.start()

    new_listings = []
    print(f"Existing company names: {existing_company_names}")
    for job in extraction_result:
        # Extract company name from the title (take text before first '|')
        title = job.get("title", "")
        company_name = title.split("|")[0].strip()

        if company_name in existing_company_names:
            print(f"Skipping {company_name} because it already exists")
            continue

        new_listings.append(job)

    parser = HNJobParser(new_listings)
    results = parser.start()

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    df.to_csv("output/hn_jobs.csv", index=False)

    print(f"Saved {len(results)} jobs to output/hn_jobs.csv")


if __name__ == "__main__":
    asyncio.run(main())
