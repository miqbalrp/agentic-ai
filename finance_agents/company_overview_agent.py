from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from utils.api_client import retrieve_from_endpoint

load_dotenv()

@function_tool
def get_company_overview(ticker: str) -> str:
    """
    Get company overview only from IDX
    """
    url = f"https://api.sectors.app/v1/company/report/{ticker}/?sections=overview"

    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
company_overview_agent = Agent(
    name="Company Overview Agent",
    instructions="Return the a short narative overview of the company from the output of assigned tool.",
    tools=[get_company_overview],
    output_type=str,
    tool_use_behavior="run_llm_again"
)

async def run_company_overview_agent(input_promt: str) -> str:
    result = await Runner.run(
        company_overview_agent,
        input_promt
    )
    return result.final_output


