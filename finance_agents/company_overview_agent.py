from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

from schemas.finance_app import TextOnlyOutput
from utils.api_client import retrieve_from_endpoint
from utils.config import setup_openai_api_key, setup_sectors_api_key

import logging

setup_openai_api_key()
setup_sectors_api_key()

logger = logging.getLogger(__name__)

@function_tool
def get_company_overview(ticker: str) -> str:
    """
    Get company overview only from IDX
    """
    url = f"https://api.sectors.app/v1/company/report/{ticker}/?sections=overview"

    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        logger.error(f"Error retrieving company overview for {ticker}: {e}")
        print(f"Error retrieving company overview for {ticker}: {e}")
        return None
    
company_overview_agent = Agent(
    name="Company Overview Agent",
    instructions="Return the a narative overview of the company from the output of assigned tool.",
    tools=[get_company_overview],
    output_type=TextOnlyOutput,
    tool_use_behavior="run_llm_again"
)

async def run_company_overview_agent(input_promt: str) -> str:
    result = await Runner.run(
        company_overview_agent,
        input_promt
    )
    return result.final_output
