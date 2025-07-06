from agents import Agent, Runner, function_tool

from datetime import date
from dataclasses import dataclass
from typing import Literal

from finance_agents.company_overview_agent import company_overview_agent
from finance_agents.trend_analysis_agent import trend_analysis_agent
from finance_agents.top_companies_list_agent import top_company_ranked_agent

from finance_agents.input_guardrails import idx_only_query_guardrail, compliance_guardrail

from schemas.finance_app import GeneralizedOutput

from utils.config import setup_openai_api_key, setup_sectors_api_key
setup_openai_api_key()
setup_sectors_api_key()

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
async def get_company_daily_transaction(ticker: str, metrics: str, date_period: str) -> str:
    """
    A tool to run trend analysis on daily transaction for a company.

    Args:
        ticker (str): The stock ticker of the company.
        metrics (str): The metrics to analyze, such as "volume" or "price".
        date_period (str): The date range for the analysis as in the user query.
    """

    agent = trend_analysis_agent
    result = await Runner.run(
        agent,
        f"Analyze {metrics} for {ticker} in the time period {date_period}."
    )
    return result.final_output

# Define agent as a tool to get top companies ranked by market cap
@function_tool
async def get_top_companies_ranked(
    n: int,
    sort_by: str,
    year: int
) -> str:
    """
    A tool to retrieve top companies ranked by 
        - Dividend yield
        - Earnings
        - Market cap
        - Revenue
        - Total dividend
        - PB / PE / PS ratios
    Args:
        n (int): The number of top companies to retrieve.
        sort_by: The criteria to sort the companies.
    """

    agent = top_company_ranked_agent
    result = await Runner.run(
        agent,
        f"Provide a list of the top {n} companies ranked by {sort_by} in year {year}."
    )
    return result.final_output

# Define the orchestrator agent that uses the above tools
orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=
    "Your task is to understand the user's query and respond using the tools provided. "
    "Always pass the full user query as input to any tool you invoke. "
    "You must rely exclusively on the available tools to answer the query — do not generate responses independently. "
    f"The current date is {date.today()}. "
    "If none of the tools are suitable for the query, clearly inform the user that it is out of scope for this application. "
    "All responses must strictly follow the GeneralizedOutput schema. Do not generate or return images for charts or visualizations. "
    "If multiple tools are used, provide a clear and concise summary of their combined outputs.",
    tools=[
        get_company_overview,
        get_company_daily_transaction,
        get_top_companies_ranked
    ],
    output_type=GeneralizedOutput,
    input_guardrails=[
        idx_only_query_guardrail,
        # compliance_guardrail
    ]
)

async def run_orchestrator_agent(input_promt: str) -> GeneralizedOutput:
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