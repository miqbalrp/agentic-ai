from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from utils.api_client import retrieve_from_endpoint
from datetime import date

from schemas.finance_app import AnalysisWithPlotOutput

import pandas as pd
import plotly.express as px

load_dotenv()

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
        "Provide a dataset of daily transaction values and an analysis of them. "
        "Never return a chart as an image."
        "Your task is to generate structured data for **line chart for time-series data** "
        "along with a suitable plot title, "
        "axis labels, and a brief analysis. "
        "Strictly adhere to the AnalysisWithPlotOutput schema. "
        "For 'line_chart' charts: "
        "- 'x' should be dates in 'YYYY-MM-DD' format (strings). "
        "- 'y' should be numerical values (floats). "
        "- Set 'chart_type' to 'line_chart'. "
        "Do NOT include any additional conversational text outside the JSON output. "
        "Always provide relevant 'axis_labels'."
        "Infer the date range from the input. " \
        "Use get_past_n_days tool to get the starting date based on user query." \
        # "If user gives no particular range, set the default as 30 days." \
        "Today's date is "+ get_today_date(),
    tools=[get_daily_transaction, 
           get_past_n_days
           ],
    tool_use_behavior="run_llm_again",
    output_type=AnalysisWithPlotOutput
)

async def run_trend_analysis_agent(input_promt: str) -> AnalysisWithPlotOutput:
    result = await Runner.run(
        trend_analysis_agent,
        input_promt
    )
    return result.final_output