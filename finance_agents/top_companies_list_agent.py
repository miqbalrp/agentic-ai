from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from utils.api_client import retrieve_from_endpoint
from datetime import date

from schemas.finance_app import TopCompanyClassification, AnalysisWithPlotOutput

import pandas as pd
import plotly.express as px

load_dotenv()

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
        "Provide a dataset of top companies ranked by specific classification and an analysis of them. "
        "Your task is to generate structured data for **horizontal bar chart** "
        "along with a suitable plot title, "
        "axis labels, and a brief analysis. "
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