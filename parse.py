from schemas import HackerNewsExtractedJob
import json
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional

client = OpenAI(api_key="sk-proj-Dt6FeI1B0aurKP8kTHV4T3BlbkFJXh2Ld8cxMM8Ol4VPtmcx")

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
        print(response.choices[0].message.content)
        return json.loads(response.choices[0].message.content)



    def start(self):
        print(f'starting parse for {len(self.extracted_jobs)} jobs')

        results = []
        i = 0
        for job in self.extracted_jobs:
            i += 1
            if i > 5:
                break
            parsed_job = self.parse_content(job.get("job_content_html"))
            roles = parsed_job.get("roles", [])

            # Create a entry for each role
            for role in roles:
                email = role.get("email")
                if email:
                    email = email.replace("at", "@").replace("dot", ".").replace(" ", "")

                results.append({
                    "company_name": parsed_job.get("company_name", ""),
                    "website": parsed_job.get("website", ""),
                    "location": parsed_job.get("location", ""),
                    "role": role.get("title", ""),
                    "salary": role.get("salary", 0),
                    "email": role.get("email"),
                    "apply_link": role.get("apply_link"),
                })

        print(f'finished parse for {len(results)} jobs')
        return results

