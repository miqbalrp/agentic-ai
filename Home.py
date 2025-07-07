import streamlit as st
import asyncio

from agents import trace, InputGuardrailTripwireTriggered
from finance_agents.planner_executor_agent import run_planner_agent, run_executor_agent
from schemas.finance_app import TextOnlyOutput, AnalysisWithPlotOutput, GeneralizedOutput
from utils.display_functions import *
from utils.config import setup_openai_api_key, setup_sectors_api_key  # Ensure config is loaded to set up API keys
import logging

setup_openai_api_key()  # Set up OpenAI API key
setup_sectors_api_key()  # Set up Sectors API key

logging.basicConfig(
    level=logging.INFO,  # You can change to DEBUG for more detail
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("agentic_app.log"),  # Log to a file
        logging.StreamHandler()  # Also print logs in terminal
    ]
)
logger = logging.getLogger(__name__)

def main():
    set_title_and_sidebar()
    initialize_session_state()  # Initialize session state variables
    display_example_queries()  # Display example queries as selectable pills
    user_input = display_user_input_area()  # Display text area for user input
    
    if st.button("Submit"):
        set_run_query_state()  # Set the session state to indicate that a query should be run

    if st.session_state.run_query and st.session_state.user_input.strip():
        with st.spinner("Thinking...", show_time=True):
            try:
                logger.info(f"User query received: {st.session_state.user_input}")
                with trace("Finance Agents Workflow"):
                    logger.info("Running planner agent...")
                    planner_result = asyncio.run(run_planner_agent(user_input))
                    logger.info("Planner agent response received.")
                    if planner_result.execute_steps:
                        logger.info("Executing steps with executor agent...")
                        logger.info(f"User query: {planner_result.user_query}")
                        logger.info(f"Steps to execute: {planner_result.steps}")

                        # Assume planner_result.steps is a list of step descriptions
                        steps_text = "\n".join(planner_result.steps) if isinstance(planner_result.steps, list) else str(planner_result.steps)

                        st.info(
                            f"""
                            Executing steps with executor agent...
                            Steps to execute:
                            {steps_text}
                            """
                        )

                        # Run the executor agent with the steps from the planner agent
                        executor_input = f"User query: {planner_result.user_query}\nSteps to execute: {planner_result.steps}"
                        executor_result = asyncio.run(run_executor_agent(executor_input))
                        if isinstance(executor_result, GeneralizedOutput):
                            display_agent_response_title()
                            st.write(executor_result.summary)
                            if executor_result.plot_data:
                                display_analysis_with_plot_output(executor_result.plot_data)
                        else:
                            display_agent_response_title()
                            st.write(executor_result)
                        logger.info("Executor agent response displayed.")
                    else:
                        logger.info("Planner agent decided not to execute steps.")
                        logger.info(f"Reason: {planner_result.reason}")
                        display_agent_response_title()
                        st.write(planner_result.reason)
            
            # Handle input guardrails
            except InputGuardrailTripwireTriggered as e:
                print(e)
                info = e.guardrail_result.output.output_info
                message=f"Input blocked by {info.guardrail} guardrail: {info.reason}" + (f"\nDetails: {info.details}" if info.details else "")
                logger.warning(f"Input guardrail triggered: {message}")
                st.info(f"❌ Input blocked: {message}")
            
            # Handle other exceptions
            except Exception as e:
                logger.error(f"Error during agent execution: {e}", exc_info=True)
                st.info("Please try again or try a different query.")

        st.session_state.run_query = False  # Reset after query

if __name__ == "__main__":
    main()

