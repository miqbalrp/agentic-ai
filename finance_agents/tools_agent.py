from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

from schemas.finance_app import *
from utils.api_client import retrieve_from_endpoint
import logging

import pandas as pd
import plotly.express as px
from date import date

logger = logging.getLogger(__name__)

# Define company overview agent

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

# Define trend analysis agent

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

trend_analysis_agent_instruction = """ \
    Your task is to generate a structured dataset representing daily transaction values over time, 
    intended for use in a line chart. 
    Do not return any chart as an image. 
    You must provide: a well-structured time-series dataset, a descriptive plot title, clear axis labels, 
    and a meaningful analysis that explains patterns, trends, or anomalies in the data.
    Ensure the output is suitable for programmatic rendering in a Plotly line chart.
    Strictly adhere to the AnalysisWithPlotOutput schema. 
    For 'line_chart' charts: 
    - 'x' should be dates in 'YYYY-MM-DD' format (strings). 
    - 'y' should be numerical values (floats). 
    - Set 'chart_type' to 'line_chart'. 
    Do NOT include any additional conversational text outside the JSON output. 
    Always provide relevant 'axis_labels'.
    Infer the date range from the input.  
    Use get_past_n_days tool to get the starting date based on user query. 
    Today's date is """+ get_today_date()

trend_analysis_agent = Agent(
    name="Daily Transaction Agent",
    instructions= trend_analysis_agent_instruction,
    tools=[get_daily_transaction, get_past_n_days],
    tool_use_behavior="run_llm_again",
    output_type=AnalysisWithPlotOutput
)

# Define top companies list

@function_tool
def get_top_companies_ranked_by_classification(classification: TopCompanyClassification, number_of_stock:int=3, year:int=2025):
    """
    Get top companies based on classification mentioned by query. 
    """
    url = f"https://api.sectors.app/v1/companies/top/?classifications={classification}&n_stock={number_of_stock}&year={year}"
    
    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

top_company_ranked_agent_instruction = (
    "Your task is to generate a structured dataset representing the top companies ranked by a specific classification or metric. "
    "The data should be formatted for visualization in a horizontal bar chart. "
    "Include a descriptive plot title, clearly labeled axes, and a concise analysis summarizing key insights or comparisons from the ranking. "
    "Ensure the output is suitable for rendering programmatically — do not return charts as images."
    "Strictly adhere to the AnalysisWithPlotOutput schema. "
    "For 'bar_horizontal_chart' charts: "
    "- 'y' should be list of the companies ticker. "
    "- 'x' should be numerical values (floats). "
    "- Set 'chart_type' to 'bar_horizontal_chart'. "
    "Do NOT include any additional conversational text outside the JSON output. "
    "Always provide relevant 'axis_labels'."
)

top_company_ranked_agent = Agent(
    name="Top Company Ranked Agent",
    instructions=top_company_ranked_agent_instruction,
    tools=[get_top_companies_ranked_by_classification],
    tool_use_behavior="run_llm_again",
    output_type=AnalysisWithPlotOutput
)
