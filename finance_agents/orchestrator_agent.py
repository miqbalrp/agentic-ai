from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

from datetime import date
from dataclasses import dataclass
from typing import Literal

from finance_agents.company_overview_agent import company_overview_agent
from finance_agents.trend_analysis_agent import trend_analysis_agent
from finance_agents.top_companies_list_agent import top_company_ranked_agent

from schemas.finance_app import GeneralizedOutput

load_dotenv()

# Define agent as a tool to get company overview
@function_tool
async def get_company_overview(ticker: str) -> str:
    """
    A tool to retrieve company overview.

    Args:
        ticker (str): The stock ticker of the company.
    """

    agent = company_overview_agent
    result = await Runner.run(
        agent,
        f"Provide a summary overview for the company with ticker {ticker}."
    )
    return result.final_output

# Define agent as a tool to get daily transaction analysis
@function_tool
async def get_company_daily_transaction(ticker: str, date_period: str) -> str:
    """
    A tool to run trend analysis on daily transaction for a company.

    Args:
        ticker (str): The stock ticker of the company.
        date_period (str): The date range for the analysis as in the user query.
    """

    agent = trend_analysis_agent
    result = await Runner.run(
        agent,
        f"Analyze the daily transaction for {ticker} in the time period {date_period}."
    )
    return result.final_output

# Define the orchestrator agent that uses the above tools
orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=
    "Understand the query from users and use the tools given to you to answer the user query. " \
    "Always pass a complete user query to each tool that used as input." \
    "If the query required get_company_daily_transaction tool to be called, provide the ticket and date range based on the query." \
    "If the query required get_company_overview tool to be called, provide the company ticker based on the query." \
    "If no appropriate tool, return inform the user that the query is out of the scope of this app." \
    "Strictly adhere to the GeneralizedOutput schema. Never return an image for chart or visualization." \
    "If multiple tools have been used, summarized the output.",
    tools=[
        get_company_overview,
        get_company_daily_transaction
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