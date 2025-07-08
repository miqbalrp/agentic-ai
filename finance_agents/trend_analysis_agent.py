from agents import Agent, Runner, function_tool
from utils.api_client import retrieve_from_endpoint
from datetime import date

from schemas.finance_app import AnalysisWithPlotOutput

import pandas as pd
import plotly.express as px

def get_today_date() -> str:
    """
    Get today's date
    """
    today = date.today()
    return today.strftime("%Y-%m-%d")

@function_tool
def get_past_n_days(past_n_days: int) -> str:
    """
    Get the date n days ago from today
    """
    today = date.today()
    past_date = today - pd.Timedelta(days=past_n_days)
    return past_date.strftime("%Y-%m-%d")

@function_tool
def get_daily_transaction(ticker: str, start_date: str, end_date: str) -> str:
    """
    Get daily transaction for an IDX stock
    """
    url = f"https://api.sectors.app/v1/daily/{ticker}/?start={start_date}&end={end_date}"
    
    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

trend_analysis_agent = Agent(
    name="Daily Transaction Agent",
    instructions=
        "Your task is to generate a structured dataset representing daily transaction values over time, "
        "intended for use in a line chart. "
        "Do not return any chart as an image. "
        "You must provide: a well-structured time-series dataset, a descriptive plot title, clear axis labels, "
        "and a meaningful analysis that explains patterns, trends, or anomalies in the data."
        "Ensure the output is suitable for programmatic rendering in a Plotly line chart."
        "Strictly adhere to the AnalysisWithPlotOutput schema. "
        "For 'line_chart' charts: "
        "- 'x' should be dates in 'YYYY-MM-DD' format (strings). "
        "- 'y' should be numerical values (floats). "
        "- Set 'chart_type' to 'line_chart'. "
        "Do NOT include any additional conversational text outside the JSON output. "
        "Always provide relevant 'axis_labels'."
        "Infer the date range from the input. " \
        "Use get_past_n_days tool to get the starting date based on user query." \
        "Today's date is "+ get_today_date(),
    tools=[get_daily_transaction, get_past_n_days],
    tool_use_behavior="run_llm_again",
    output_type=AnalysisWithPlotOutput
)

async def run_trend_analysis_agent(input_promt: str) -> AnalysisWithPlotOutput:
    result = await Runner.run(
        trend_analysis_agent,
        input_promt
    )
    return result.final_output

if __name__ == "__main__":
    import asyncio

    from utils.config import setup_openai_api_key, setup_sectors_api_key
    setup_openai_api_key()
    setup_sectors_api_key()

    ticker = input("Enter stock ticker: ")
    past_n_days = int(input("Enter number of past days: "))
    
    start_date = asyncio.run(get_past_n_days(past_n_days))
    end_date = get_today_date()

    result = asyncio.run(run_trend_analysis_agent(f"Analyze daily transaction for {ticker} from {start_date} to {end_date}."))
    print(result)