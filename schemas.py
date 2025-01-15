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