import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig

async def start_extraction():
    browser_config = BrowserConfig()  # Default browser configuration

    schema = {
        "name": "Jobs",
        "baseSelector": "tr.athing.comtr",
        "fields": [
            {
                "name": "job_content",
                "selector": "div.commtext",
                "type": "text",
            },
            {
                "name": "posted_by",
                "selector": "a.hnuser",
                "type": "text",
            },
            {
                "name": "posted_",
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
        print(json.dumps(data[0], indent=2) if data else "No data found")
        return data
