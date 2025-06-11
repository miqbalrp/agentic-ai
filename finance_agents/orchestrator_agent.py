from agents import Agent, Runner
from dotenv import load_dotenv

from datetime import date
from dataclasses import dataclass
from typing import Literal

from finance_agents.company_overview_agent import company_overview_agent
from finance_agents.trend_analysis_agent import trend_analysis_agent
from finance_agents.top_companies_list_agent import top_company_ranked_agent

from schemas.finance_app import GeneralizedOutput

load_dotenv()

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=
    "Understand the query from users and use the tools given to you to answer the user query. " \
    "If no appropriate tool, return inform the user that the query is out of the scope of this app." \
    "Strictly adhere to the GeneralizedOutput schema. Never return an image for chart or visualization." \
    "If multiple tools have been used, summarized the output.",
    tools=[
        company_overview_agent.as_tool(
            tool_name="get_company_overview",
            tool_description="Retrieve company summary overview."
        ),
        trend_analysis_agent.as_tool(
            tool_name="get_company_daily_transaction",
            tool_description="Provide the trend and the analysis of daily transaction of a company."
        )
    ],
    output_type=GeneralizedOutput
)

async def run_orchestrator_agent(input_promt: GeneralizedOutput):
    result = await Runner.run(
        orchestrator_agent,
        input_promt
    )
    return result.final_output

if __name__ == "__main__":
    import asyncio
    query = input("Input query:")
    result = asyncio.run(run_orchestrator_agent(query))
    print(result)