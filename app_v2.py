import streamlit as st
import asyncio

from agents import trace
from finance_agents.orchestrator_agent import run_orchestrator_agent
from schemas.finance_app import TextOnlyOutput, AnalysisWithPlotOutput, GeneralizedOutput

import pandas as pd
import plotly.express as px

import logging
import logging

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
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "run_query" not in st.session_state:
        st.session_state.run_query = False

    # Title and description
    st.title("IDX AI Assistant 📈")
    st.caption("📘 You can ask about IDX-listed companies, such as a company's summary overview, daily transaction trends, or top-ranked companies based on specific metrics (e.g., revenue or market cap).")

    # Example queries
    st.markdown("###### Try an example query:")
    example_queries = [
        "Show me summary of TLKM", 
        "Analyze daily closing price of BBCA in the last 14 days!",
        "Top 5 companies by earning in 2024"
    ]

    for example in example_queries:
        if st.button(f"{example}"):
            st.session_state.user_input = example
            st.session_state.run_query = False  # Ensure it doesn't trigger submission
            st.rerun()

    # User input
    user_input = st.text_area(
        "💬 What would you like to know?", 
        value=st.session_state.user_input,
        key="user_input_text",
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
                
            except Exception as e:
                logger.error(f"Error during agent execution: {e}", exc_info=True)
                st.info("Please try again or try a different query.")
        
    st.markdown("""
    ---
    🔧 **Powered by**:  
    [OpenAI API](https://platform.openai.com/docs) | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | [Plotly](https://plotly.com/python/) | [Sectors.app API](https://sectors.app) | [Streamlit](https://streamlit.io)

    💻 **Source Code**: [GitHub Repository](https://github.com/miqbalrp/agentic-ai)
    """)

if __name__ == "__main__":
    main()