import streamlit as st
import asyncio

from finance_agents.triage_agent import run_triage_agent
from schemas.finance_app import TextOnlyOutput, AnalysisWithPlotOutput

import pandas as pd
import plotly.express as px

st.title("Stock Analysis with Agentic AI")
user_input = st.text_input("Enter your query:")

if user_input:
    with st.spinner("Thinking..."):
        agent_response = asyncio.run(run_triage_agent(user_input))
        if isinstance(agent_response, TextOnlyOutput):
            text_output: TextOnlyOutput = agent_response
            st.markdown("### 🤖 Agent's Response")
            st.write(text_output.summary)
        elif isinstance(agent_response, AnalysisWithPlotOutput):
            plot_output: AnalysisWithPlotOutput = agent_response

            st.markdown("### 🤖 Agent's Response")
            st.write(plot_output.summary)

            x_axis_label = plot_output.axis_labels.x_axis_title
            y_axis_label = plot_output.axis_labels.y_axis_title
            plot_title = plot_output.plot_title

            rows = []
            for dataset in plot_output.plot_data:
                x_vals = dataset.x
                y_vals = dataset.y
                # Use dataset.category if available, else create a list of "Series"
                if dataset.category:
                    category_vals = dataset.category
                else:
                    category_vals = ["Series"] * len(x_vals)
                
                for x_val, y_val, cat in zip(x_vals, y_vals, category_vals):
                    rows.append({
                        "x_data": x_val,
                        "y_data": y_val,
                        "category": cat
                    })

            df = pd.DataFrame(rows)

            fig = px.line(
                df, 
                x="x_data", 
                y="y_data", 
                markers=True, 
                labels={'x_data': x_axis_label, 'y_data': y_axis_label},
                title=plot_title,
                color="category"
                )
            st.plotly_chart(fig)

        else: 
            print("No output")