from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union

# Define simple all text output type 
class TextOnlyOutput(BaseModel):
    """
    Class for simple output that consist only text without visualization. Used for summary overview of companies.
    """
    summary: str

# Define list of classification for Top Companies agent
TopCompanyClassification = Literal["dividend_yield", "earnings", "market_cap", "pb", "pe", "ps"]

# Define output with visualization
ChartType = Literal["line_chart", "bar_horizontal_chart"]

class PlotlyTraceData(BaseModel):
    x: List[Union[str, float]] = Field(
        description="List of X-axis values. For 'line_chart', these should be dates (YYYY-MM-DD). For 'bar_horizontal_chart', these should be categories (strings)."
    )
    y: List[Union[str, float]] = Field(
        description="List of Y-axis values. For 'line_chart', these are numerical values. For 'bar_horizontal_chart', these are numerical values (for the length of the bars)."
    )
    category: Optional[List[str]] = Field(
        description="Category of line chart for muultple series line chart, eg; ticker."
    )
    chart_type: ChartType = Field(
        description="The type of chart to generate. 'line_chart' for time-series data, 'bar_horizontal_chart' for categorical data."
    )
    plot_title: str = Field(description="The title of the Plotly chart. Should have a clear short explanation of the chart.")
    x_axis_title: str = Field(description="Title for the X-axis.")
    y_axis_title: str = Field(description="Title for the Y-axis.")

class PlotlyAxisLabels(BaseModel):
    x_axis_title: Optional[str] = Field(default=None, description="Title for the X-axis.")
    y_axis_title: Optional[str] = Field(default=None, description="Title for the Y-axis.")

class AnalysisWithPlotOutput(BaseModel):
    summary: str = Field(description="A textual analysis or summary of the plot data.")
    plot_data: List[PlotlyTraceData] = Field(
        description="A list of data objects, each representing a trace for a Plotly figure. Contains data formatted for the specified chart_type."
    )

class GeneralizedOutput(BaseModel):
    summary: str = Field(description="A narative summary of the output.")
    plot_data: Optional[List[PlotlyTraceData]] = Field(
        description="A list of data objects, each representing a trace for a Plotly figure. Contains data formatted for the specified chart_type."
    )

# Define the standardized output information for guardrail violations
class GuardrailViolationInfo(BaseModel):
    guardrail: str = Field(description="Name or type of the guardrail triggered.")
    violated: bool = Field(description="Whether the guardrail was violated.")
    reason: str = Field(description="Explanation of the violation.")
    details: str = Field(default="", description="Additional context or details.")
