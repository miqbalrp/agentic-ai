import streamlit as st
import asyncio

from agents import trace, InputGuardrailTripwireTriggered
from finance_agents.orchestrator_agent import run_orchestrator_agent
from schemas.finance_app import TextOnlyOutput, AnalysisWithPlotOutput, GeneralizedOutput

import pandas as pd
import plotly.express as px

from utils.config import setup_openai_api_key, setup_sectors_api_key  # Ensure config is loaded to set up API keys
import logging

setup_openai_api_key()  # Set up OpenAI API key
setup_sectors_api_key()  # Set up Sectors API key

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # You can change to DEBUG for more detail
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("agentic_app.log"),  # Log to a file
        logging.StreamHandler()  # Also print logs in terminal
    ]
)
logger = logging.getLogger(__name__)

def display_agent_response_title():
    st.markdown("### 🤖 Agent's Response")

def display_text_only_output(text_output: TextOnlyOutput):
    display_agent_response_title()
    st.write(text_output.summary)

def display_analysis_with_plot_output(plot_data):
    for dataset in plot_data:
        plot_title = dataset.plot_title
        x_axis_label = dataset.x_axis_title
        y_axis_label = dataset.y_axis_title

        df = pd.DataFrame({
            "x_data": dataset.x,
            "y_data": dataset.y
            }
        )

        if dataset.chart_type == 'line_chart':
            fig = px.line(
                df, 
                x="x_data", 
                y="y_data", 
                markers=True, 
                labels={'x_data': x_axis_label, 'y_data': y_axis_label},
                title=plot_title
                )
            st.plotly_chart(fig)

        elif dataset.chart_type == 'bar_horizontal_chart':
            y_label_order = df['y_data'].tolist()
            fig = px.bar(
                df, 
                x="x_data", 
                y="y_data", 
                orientation="h",
                labels={'x_data': x_axis_label, 'y_data': y_axis_label},
                title=plot_title,
                category_orders={'y_data': y_label_order}
                )
            st.plotly_chart(fig)

def main():
    st.set_page_config(
        page_title="IDX AI Assistant",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "run_query" not in st.session_state:
        st.session_state.run_query = False
    if "example_query_pills" not in st.session_state:
        st.session_state.example_query_pills = None

    # Title and description
    st.title("📈 IDX AI Assistant")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
    You can ask about:

    - 📄 **Company overview**
    - 📈 **Daily transaction trends** , including:
        - Closing price
        - Transaction volume
        - Market cap
    - 🏆 **Top-ranked companies** by metrics like:
        - Dividend yield
        - Earnings
        - Market cap
        - Revenue
        - Total dividend
        - PB / PE / PS ratios
                        
    **Currently supports companies listed on the Indonesia Stock Exchange (IDX) only.**
    **Data is retrieved from [Sectors.app](https://sectors.app) API.**
                        """)
    st.sidebar.markdown("""
    ---
    🔧 **Powered by**:  
    [OpenAI API](https://platform.openai.com/docs) | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | [Plotly](https://plotly.com/python/) | [Sectors.app API](https://sectors.app) | [Streamlit](https://streamlit.io)

    💻 **Source Code**: [GitHub Repository](https://github.com/miqbalrp/agentic-ai)
    """)

    # Example queries    
    def on_pill_change():
        """Callback function to handle pill selection change."""
        st.session_state.user_input = st.session_state.example_query_pills

    example_queries = [
        "Show me summary of TLKM", 
        "Analyze daily closing price of BBCA in the last 14 days!",
        "Top 5 Indonesia companies by earning in 2024"
    ]
    st.pills(
        label="Try an example query:",
        options=example_queries,
        selection_mode="single",
        key="example_query_pills",
        on_change=on_pill_change
    )

    # User input
    user_input = st.text_area(
        "💬 What would you like to know?", 
        value=st.session_state.user_input,
        key="user_input",
        help="E.g., 'Show me daily transaction of BBCA in the past month'")
    
    if st.button("Submit"):
        st.session_state.run_query = True

    if st.session_state.run_query and st.session_state.user_input.strip():
        with st.spinner("Thinking..."):
            try:
                logger.info(f"User query received: {st.session_state.user_input}")
                with trace("Finance Agents Workflow"):
                    logger.info("Running orchestrator agent...")
                    agent_response = asyncio.run(run_orchestrator_agent(user_input))
                    logger.info("Agent response received.")
                    if isinstance(agent_response, GeneralizedOutput):
                        display_agent_response_title()
                        st.write(agent_response.summary)
                        if agent_response.plot_data:
                            display_analysis_with_plot_output(agent_response.plot_data)
                    else:
                        display_agent_response_title()
                        st.write(agent_response)
        
            except InputGuardrailTripwireTriggered as e:
                print(e)
                info = e.guardrail_result.output.output_info
                message=f"Input blocked by {info.guardrail} guardrail: {info.reason}" + (f"\nDetails: {info.details}" if info.details else "")
                logger.warning(f"Input guardrail triggered: {message}")
                st.info(f"❌ Input blocked: {message}")


            except Exception as e:
                logger.error(f"Error during agent execution: {e}", exc_info=True)
                st.info("Please try again or try a different query.")
        
        st.session_state.run_query = False  # Reset after query

if __name__ == "__main__":
    main()