import asyncio
import pandas as pd
from typing import List, Set, Dict, Any

from extract import HackerNewsJobExtractor
from parse import HNJobParser
from files import FileHelper


class JobDeduplicator:
    def __init__(self, previous_listings: pd.DataFrame | None):
        self.existing_companies: Set[str] = set()
        if isinstance(previous_listings, pd.DataFrame) and not previous_listings.empty:
            self._load_existing_companies(previous_listings)
    
    def _load_existing_companies(self, df: pd.DataFrame) -> None:
        """Load existing company names from previous listings DataFrame."""
        if "company_name" in df.columns:
            self.existing_companies.update(df["company_name"].values)
    
    def filter_new_listings(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out jobs from companies that already exist in previous listings."""
        new_listings = []
        for job in jobs:
            company_name = self._extract_company_name(job)
            if company_name not in self.existing_companies:
                new_listings.append(job)
            else:
                print(f"Skipping {company_name} because it already exists")
        return new_listings
    
    def _extract_company_name(self, job: Dict[str, Any]) -> str:
        """Extract company name from job title."""
        title = job.get("title", "")
        return title.split("|")[0].strip()


async def process_jobs() -> None:
    """Main function to process and save HN job listings."""
    # Load previous listings for deduplication
    file_helper = FileHelper()
    previous_listings = file_helper.open_last_output_file()
    
    # Initialize deduplicator
    deduplicator = JobDeduplicator(previous_listings)
    print(f"Found {len(deduplicator.existing_companies)} unique companies in previous listings")
    
    # Extract new job listings
    extractor = HackerNewsJobExtractor()
    extracted_jobs = await extractor.start()
    
    # Filter out duplicate listings
    new_listings = deduplicator.filter_new_listings(extracted_jobs)
    
    # Parse and save new listings
    parser = HNJobParser(new_listings)
    parsed_jobs = parser.start()
    
    # Save results
    output_path = "output/hn_jobs.csv"
    df = pd.DataFrame(parsed_jobs)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(parsed_jobs)} jobs to {output_path}")


if __name__ == "__main__":
    asyncio.run(process_jobs())
