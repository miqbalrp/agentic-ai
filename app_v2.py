import streamlit as st
import asyncio

from agents import trace
from finance_agents.orchestrator_agent import run_orchestrator_agent
from schemas.finance_app import TextOnlyOutput, AnalysisWithPlotOutput, GeneralizedOutput

import pandas as pd
import plotly.express as px

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
    st.title("IDX Stock Analysis with Agentic AI")
    user_input = st.text_input("Enter your query:")

    if user_input:
        with st.spinner("Thinking..."):
            try:
                with trace("Finance Agents Workflow"):
                    agent_response = asyncio.run(run_orchestrator_agent(user_input))
                    print(agent_response)
                    if isinstance(agent_response, GeneralizedOutput):
                        display_agent_response_title()
                        st.write(agent_response.summary)
                        if len(agent_response.plot_data) > 0:
                            display_analysis_with_plot_output(agent_response.plot_data)
                    else:
                        display_agent_response_title()
                        st.write(agent_response)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Please try again or try a different query.")
        
    else: st.warning("Currently we provide a report of IDX companies, including: summary overview, daily transaction analysis, and top companies ranked by certain dimension.")

    st.markdown("""
    ---
    🔧 **Powered by**:  
    [OpenAI API](https://platform.openai.com/docs) | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | [Plotly](https://plotly.com/python/) | [Sectors.app API](https://sectors.app) | [Streamlit](https://streamlit.io)

    💻 **Source Code**: [GitHub Repository](https://github.com/miqbalrp/agentic-ai)
    """)

if __name__ == "__main__":
    main()