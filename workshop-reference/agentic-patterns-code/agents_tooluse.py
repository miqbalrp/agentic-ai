import os
import json
import requests
from typing import List
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()
SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")


headers = {"Authorization": SECTORS_API_KEY}
def retrieve_from_endpoint(url: str) -> dict:

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return json.dumps(data)

@function_tool
def get_company_overview(ticker: str, country: str) -> str:
    """
    Get company overview from Singapore Exchange (SGX) or Indonesia Exchange (IDX)
    """
    assert country.lower() in ["indonesia", "singapore", "malaysia"], "Country must be either Indonesia, Singapore, or Malaysia"

    if(country.lower() == "indonesia"):
        url = f"https://api.sectors.app/v1/company/report/{ticker}/?sections=overview"
    if(country.lower() == "singapore"):
        url = f"https://api.sectors.app/v1/sgx/company/report/{ticker}/"
    if(country.lower() == "malaysia"):
        url = f"https://api.sectors.app/v1/klse/company/report/{ticker}/"

    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
       
   
@function_tool
def get_top_companies_ranked(dimension: str) -> List[str]:
    """
    Return a list of top companies (symbol) based on certain dimension (dividend yield, total dividend, revenue, earnings, market cap, PB ratio, PE ratio, or PS ratio)

    @param dimension: The dimension to rank the companies by, one of: dividend_yield, total_dividend, revenue, earnings, market_cap, pb, pe, ps
    @return: A list of top tickers in a given year based on certain classification
    """

    url = f"https://api.sectors.app/v1/companies/top/?classifications={dimension}&n_stock=3"

    return retrieve_from_endpoint(url)


company_research_agent = Agent(
    name="company_research_agent",
    instructions="Research the company based on the ticker provided.",
    tools=[get_company_overview, get_top_companies_ranked],
    tool_use_behavior="run_llm_again"
)

async def main():
    # query = "Tell me about the company listed on Singapore Exchange with ticker 'D05'."
    query = "Find me top 7 companies in Indonesia based on dividend_yield, only return the ticker."
    result = await Runner.run(
        company_research_agent,
        query
    )
    print(f"👧: {query}")
    print(f"🤖: {result.final_output}")
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())