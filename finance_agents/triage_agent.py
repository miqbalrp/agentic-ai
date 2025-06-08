from agents import Agent, Runner
from dotenv import load_dotenv

from datetime import date
from dataclasses import dataclass
from typing import Literal

load_dotenv()

@dataclass
class TriageOutput:
    query_type: Literal["company_overview", "trend_analysis", "top_companies_list"]

triage_agent = Agent(
    name="Triage Agent",
    instructions="Understand the query from users and decide what is the category of this query.",
    output_type=TriageOutput
)

async def run_triage_agent(input_promt: str) -> str:
    result = await Runner.run(
        triage_agent,
        input_promt
    )
    return result.final_output