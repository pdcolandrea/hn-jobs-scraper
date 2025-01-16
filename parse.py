from schemas import HackerNewsExtractedJob
import json
import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class JobRole(BaseModel):
    title: str
    salary: Optional[int]
    email: Optional[str]
    apply_link: Optional[str]


class HackerNewsJobContent(BaseModel):
    company_name: str
    website: str
    content: str
    location: str
    programming_languages: Optional[list[str]]
    roles: list[JobRole]


class HNJobParser:
    def __init__(self, extracted_jobs: list[HackerNewsExtractedJob]):
        self.extracted_jobs = extracted_jobs

    def parse_content(self, content: str):
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract the job information."},
                {"role": "user", "content": content},
            ],
            response_format=HackerNewsJobContent,
        )

        # TODO: Parse as actual schema
        return json.loads(response.choices[0].message.content)

    def start(self):
        print(f"starting parse for {len(self.extracted_jobs)} jobs")

        results = []
        for job in self.extracted_jobs:
            parsed_job = self.parse_content(job.get("job_content_html"))
            roles = parsed_job.get("roles", [])

            # Create a entry for each role
            for role in roles:
                email = role.get("email")
                if email:
                    email = (
                        email.replace("at", "@").replace("dot", ".").replace(" ", "")
                    )

                results.append(
                    {
                        "company_name": parsed_job.get("company_name", ""),
                        "website": parsed_job.get("website", ""),
                        "location": parsed_job.get("location", ""),
                        "role": role.get("title", ""),
                        "programming_languages": parsed_job.get(
                            "programming_languages", []
                        ),
                        "salary": role.get("salary", 0),
                        "email": email,
                        "apply_link": role.get("apply_link"),
                        "og_content": parsed_job.get("content", ""),
                    }
                )

        print(f"finished parse for {len(results)} jobs")
        return results
