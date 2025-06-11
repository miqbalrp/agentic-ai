from agents import Agent, Runner
from dotenv import load_dotenv

from datetime import date
from dataclasses import dataclass
from typing import Literal

from finance_agents.company_overview_agent import company_overview_agent
from finance_agents.trend_analysis_agent import trend_analysis_agent
from finance_agents.top_companies_list_agent import top_company_ranked_agent

load_dotenv()

triage_agent = Agent(
    name="Triage Agent",
    instructions=
    "Understand the query from users and handoff the analysis to appropriate agent. " \
    "If no appropriate agent, return inform the user that the query is out of the scope of this app.",
    handoffs=[company_overview_agent, trend_analysis_agent, top_company_ranked_agent]
)

async def run_triage_agent(input_promt: str):
    result = await Runner.run(
        triage_agent,
        input_promt
    )
    return result.final_output