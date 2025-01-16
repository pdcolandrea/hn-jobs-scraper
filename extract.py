import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig
from bs4 import BeautifulSoup

from schemas import HackerNewsExtractedJob


class HackerNewsJobExtractor:
    def __init__(self):
        pass

    async def start(self) -> list[HackerNewsExtractedJob]:
        browser_config = BrowserConfig()

        schema = {
            "name": "Jobs",
            "baseSelector": "tr.athing.comtr",
            "fields": [
                {
                    "name": "indent",
                    "selector": "td.ind",
                    "type": "html",
                },
                {
                    "name": "job_content",
                    "selector": "div.commtext",
                    "type": "html",
                },
                {
                    "name": "posted_by",
                    "selector": "a.hnuser",
                    "type": "text",
                },
                {
                    "name": "posted_ago",
                    "selector": "span.age",
                    "type": "text",
                },
            ],
        }

        extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS, extraction_strategy=extraction_strategy
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://news.ycombinator.com/item?id=42575537", config=run_config
            )

            if not result.success:
                print("Crawl failed:", result.error_message)
                raise Exception(result.error_message)

            data = json.loads(result.extracted_content)

            print(f"Extracted {len(data)} job entries")
            if len(data) == 0:
                return []

            processed_jobs = self.post_process(data)

            print(f"Processed {len(processed_jobs)} job entries")
            print(
                json.dumps(processed_jobs[8], indent=2)
                if processed_jobs
                else "No data found"
            )

            return processed_jobs

    def post_process(
        self, data: list[HackerNewsExtractedJob]
    ) -> list[HackerNewsExtractedJob]:
        processed_jobs = []

        # Post-process to extract titles
        for job in data:
            # Clean up the HTML content first
            job_content = job.get("job_content")
            job["job_content_html"] = job_content
            job_content = job_content.replace('<div class="commtext c00">', "").replace(
                "</div>", ""
            )

            # Split content into parts using <p> tags
            content_parts = job_content.split("<p>")

            # First part is the title (before first <p> tag)
            title = content_parts[0].strip()

            # Join remaining parts and clean up </p> tags
            job_description = ""
            if len(content_parts) > 1:
                job_description = " ".join(content_parts[1:])
                job_description = job_description.replace("</p>", "").strip()

            # Check if this is a comment by looking at the indent
            indent_html = job.get("indent", "")
            if 'indent="0"' not in indent_html:
                continue

            # Update the job dictionary
            job["title"] = BeautifulSoup(title, "html.parser").get_text()
            job["job_content"] = BeautifulSoup(
                job_description, "html.parser"
            ).get_text()
            job["posted_by"] = job.get("posted_by", "").strip()
            job["posted_ago"] = job.get("posted_ago", "").strip()

            processed_jobs.append(job)

        return processed_jobs
