from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from utils.api_client import retrieve_from_endpoint
from datetime import date

from pydantic import BaseModel, Field
from typing import List

import pandas as pd
import plotly.express as px

load_dotenv()

def get_today_date() -> str:
    """
    Get today's date
    """
    today = date.today()
    return today.strftime("%Y-%m-%d")

class DataPoint(BaseModel):
    date: str = Field(description="The date for this data point, in YYYY-MM-DD format.")
    value: float = Field(description="The numerical value associated with this date.")

class TrendAnalysisOutput(BaseModel):
    dataset: List[DataPoint] = Field(
        description="A list of dictionaries, where each dictionary contains a 'date' and a 'value'."
    )
    analysis: str = Field(
        description="A string containing the analysis or summary of the dataset."
    )

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
        "Strictly adhere to the AgentOutput JSON schema."
        "Infer the date range from the user query. Today's date is "+ get_today_date(),
    tools=[get_daily_transaction],
    tool_use_behavior="run_llm_again",
    output_type=TrendAnalysisOutput
)

async def run_trend_analysis_agent(input_promt: str) -> TrendAnalysisOutput:
    result = await Runner.run(
        trend_analysis_agent,
        input_promt
    )
    return result.final_output

def plot_line_chart(dataset: DataPoint):
    df = pd.DataFrame([dp.model_dump() for dp in dataset])
    fig = px.line(df, x="date", y="value", markers=True, labels={'date': 'Date', 'value': 'Value'})
    return fig
