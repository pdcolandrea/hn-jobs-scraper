from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import Optional


class HackerNewsJob(BaseModel):
    name: str
    location: str
    job_title: str
    job_description: str
    programming_languages: Optional[list[str]]
    website: Optional[str]
    email: Optional[str]
    salary: Optional[str]
    apply_link: Optional[str]


class HackerNewsJobsResult(BaseModel):
    jobs: list[HackerNewsJob]


def start_firecrawl():
    app = FirecrawlApp()
    scraped_content = app.scrape_url(
        "https://news.ycombinator.com/item?id=42575537",
        {
            "formats": ["extract"],
            "extract": {
                "schema": HackerNewsJobsResult.model_json_schema(),
            },
        },
    )
    print(scraped_content)


if __name__ == "__main__":
    start_firecrawl()
