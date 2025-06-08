"""
This example demonstrates a deterministic flow, where each step is performed by an agent.

Usage: 
python 3_deterministic.py
🤖: What kind of companies are you interested in? 
👧: companies with the largest market cap
"""

import asyncio
import os
import json
import requests

from pydantic import BaseModel
from typing import List
from agents import Agent, Runner, function_tool, trace
from datetime import datetime
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

@function_tool
def csv_export(data: object) -> str:
    """
    Convert the object to a csv
    """
    import pandas as pd

    # Convert the object to a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')

    # Convert the DataFrame to a CSV saved as 'export.csv'
    df.to_csv('export.csv', index=True)
    return "Successfully exported to export.csv"

class ValidTickers(BaseModel):
    tickers: List[str]
    

get_top_companies_based_on_metric = Agent(
    name="get_top_companies_based_on_metric",
    instructions="Get the top companies based on the given metric. Return the tickers of the top companies, without the .JK suffix. Return in a List.",
    tools=[get_top_companies_ranked],
    output_type=List[str],
)

determine_companies_to_research = Agent(
    name="determine_companies_to_research",
    instructions="Generate a list of tickers (symbols) of companies to research based on the query. Tickers on IDX are exactly 4 characters long, e.g. BBCA, BBRI, TKLM",
    output_type=ValidTickers,
)

company_research_agent = Agent(
    name="company_research_agent",
    instructions="Research each company of a given list using the assigned tool, always assume indonesian companies unless otherwise specified.",
    tools=[get_company_overview],
    output_type=str
)


async def main():
    input_prompt = input(f"🤖: What kind of companies are you interested in? \n👧: ")
    # Ensure the entire workflow is a single trace
    with trace("Deterministic research flow"):
        # 1. Determine the companies ranked by certain dimension
        top_companies_ranked = await Runner.run(
            get_top_companies_based_on_metric,
            input_prompt
        )
        print("🤖:", top_companies_ranked.final_output)


        # 2. Add a gate to stop if the tickers are not valid
        assert isinstance(
            top_companies_ranked.final_output, list), "Invalid tickers"

        # 3. Research the company based on the query
        # 3.1 Append to Notes
        with open("3_research_notes.txt", "a") as f:
            f.write(f"Research on {input_prompt}:\n")
            f.write(f"Top companies: {top_companies_ranked.final_output}\n\n\n")

            for ticker in top_companies_ranked.final_output:
                print(f"🤖: Getting information on: {ticker}")
                company_research_result = await Runner.run(
                    company_research_agent,
                    ticker
                )
                if not company_research_result or not company_research_result.final_output:
                    print(f"🤖: Failed to get data for {ticker}")
                    f.write(f"❌ Failed to get data for {ticker}\n")
                    continue
                print(f"🤖: {company_research_result.final_output}")
                f.write(f"Company: {ticker}\n")
                f.write("" + company_research_result.final_output + "\n\n" + "Research Date: " + datetime.now().isoformat() + "\n\n\n")

        
        print(f"🤖: Done! I have provided the information on: {input_prompt}")
        
    
if __name__ == "__main__":
    asyncio.run(main())