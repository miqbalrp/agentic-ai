import streamlit as st
import asyncio
import uuid

from agents import trace, InputGuardrailTripwireTriggered
from finance_agents.orchestrator_agent import run_orchestrator_agent
from schemas.finance_app import TextOnlyOutput, AnalysisWithPlotOutput, GeneralizedOutput
from utils.display_functions import *
from utils.config import setup_openai_api_key, setup_sectors_api_key  # Ensure config is loaded to set up API keys
import logging

setup_openai_api_key()  # Set up OpenAI API key
setup_sectors_api_key()  # Set up Sectors API key

# Intialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat id
chat_id = uuid.uuid4().hex[:16]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            try:
                content = GeneralizedOutput.model_validate_json(message["content"])
                st.markdown(content.summary)
                if content.plot_data:
                    display_analysis_with_plot_output(content.plot_data)
            except ValueError:
                st.markdown(message["content"])


if prompt := st.chat_input("What do you want to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with trace("Finance Agents Chat Workflow Grouped", group_id=chat_id):
            chat_history = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
            
            with st.chat_message("assistant"):
                agent_response = asyncio.run(run_orchestrator_agent(chat_history))
                st.write(agent_response.summary)
                if agent_response.plot_data:
                    display_analysis_with_plot_output(agent_response.plot_data)

            # Add assistant message to chat history
            if isinstance(agent_response, GeneralizedOutput):
                agent_response_dict = agent_response.model_dump_json()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": agent_response_dict
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": agent_response
                })
    except InputGuardrailTripwireTriggered as e:
        with st.chat_message("assistant"):
            info = e.guardrail_result.output.output_info
            message=f"Input blocked by {info.guardrail} guardrail: {info.reason}" + (f"\nDetails: {info.details}" if info.details else "")
            st.markdown(f"Input guardrail triggered: {message}")
    except Exception as e:
        with st.chat_message("assistant"):
            st.write("An error occurred while processing your request. Please try again.")