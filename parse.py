from schemas import HackerNewsExtractedJob

class HNJobParser:
    def __init__(self, extracted_jobs: list[HackerNewsExtractedJob]):
        self.extracted_jobs = extracted_jobs

    def seperate_title_and_content(self, job: HackerNewsExtractedJob):
        title = job.get("job_content").split("\n")[0]
        content = job.get("job_content").split("\n")[1:]
        return title, content

    def start(self):
        for job in self.extracted_jobs:
            title, content = self.seperate_title_and_content(job)
            print(f"Title: {title}")
            print(f"Content: {content}")
