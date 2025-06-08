import streamlit as st
import asyncio

from finance_agents.triage_agent import run_triage_agent
from finance_agents.company_overview_agent import run_company_overview_agent
from finance_agents.trend_analysis_agent import run_trend_analysis_agent, TrendAnalysisOutput, plot_line_chart

st.title("Stock Analysis with Agentic AI")
user_input = st.text_input("Enter your query:")
if user_input:
    with st.spinner("Thinking..."):
        triage_response = asyncio.run(run_triage_agent(user_input))
        task_selected = triage_response.query_type

        if task_selected == "company_overview":
            agent_response = asyncio.run(run_company_overview_agent((user_input)))
            st.markdown("### 🤖 Agent's Response")
            st.write(agent_response)

        elif task_selected == "trend_analysis":
            agent_response: TrendAnalysisOutput = asyncio.run(run_trend_analysis_agent((user_input)))
            st.markdown("### 🤖 Agent's Response")
            st.write(agent_response.analysis)
            st.plotly_chart(plot_line_chart(agent_response.dataset))
            
        else:
            st.write("Sorry, the query is out of our scope.")
