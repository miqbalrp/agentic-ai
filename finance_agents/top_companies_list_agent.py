from agents import Agent, Runner, function_tool
from utils.api_client import retrieve_from_endpoint
from datetime import date

from schemas.finance_app import TopCompanyClassification, AnalysisWithPlotOutput

from utils.config import setup_openai_api_key, setup_sectors_api_key

import pandas as pd
import plotly.express as px

setup_openai_api_key()  # Set up OpenAI API key
setup_sectors_api_key()  # Set up Sectors API key


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
    
top_company_ranked_agent = Agent(
    name="Top Company Ranked Agent",
    instructions=
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
        "Always provide relevant 'axis_labels'.",
    tools=[get_top_companies_ranked_by_classification],
    tool_use_behavior="run_llm_again",
    output_type=AnalysisWithPlotOutput
)