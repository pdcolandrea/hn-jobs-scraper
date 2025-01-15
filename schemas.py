from pydantic import BaseModel
from typing import Optional

class HackerNewsExtractedJob(BaseModel):
    job_content: str
    posted_by: str
    posted_ago: str

# Not being used currently
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

# Not being used currently
class HackerNewsJobsResult(BaseModel):
    jobs: list[HackerNewsJob]