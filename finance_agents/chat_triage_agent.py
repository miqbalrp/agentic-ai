from agents import Agent, Runner

from datetime import date
from dataclasses import dataclass
from typing import Literal

from finance_agents.orchestrator_agent import orchestrator_agent

from utils.config import setup_openai_api_key, setup_sectors_api_key

setup_openai_api_key()  # Set up OpenAI API key
setup_sectors_api_key()  # Set up Sectors API key

chat_triage_agent = Agent(
    name="Chat Triage Agent",
    instructions=
    "Understand the query from user." \
    "If the query is related to IDX-listed companies, handoff the analysis to orchestrator agent." \
    "If the query is not related to IDX-listed companies, return an informative message to the user." \
    "If the query is not understood, return an informative message to the user." \
    "User can ask about:" \
    "- **Company overview**" \
    "- **Daily transaction trends** , including: Closing price, Transaction volume, Market cap"
    "- **Top-ranked companies** by metrics like:, Dividend yield, Earnings, Market cap, Revenue, Total dividend, PB / PE / PS ratios" \
    "Currently supports companies listed on the Indonesia Stock Exchange (IDX) only.**",
    handoffs=[orchestrator_agent],
    model="gpt-4o-mini",  # Use a smaller model for efficiency
)

async def run_chat_triage_agent(input_promt: str):
    result = await Runner.run(
        chat_triage_agent,
        input_promt
    )
    return result.final_output