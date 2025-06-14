# agentic-ai

A personal learning project focused on building **Agentic AI systems** using the **OpenAI Agents SDK**. This repository showcases an interactive financial analytics application that combines **multi-agent coordination**, **retrieval-augmented generation (RAG)**, and **natural language interfaces** — all powered by real stock data from [Sectors.app](https://sectors.app).

---

## Project Overview

This app demonstrates a modular agent-based workflow:

- 🧭 **Triage Agent**: Understands user questions and delegates tasks.
- 🧾 **Company Overview Agent**: Generates a narrative report of a company in IDX.
- 📊 **Trend Analyst Agent**: Uses a tool to pull real financial data via API and generate the analysis of the trend with visualization.
- and more

<img width="510" alt="image" src="https://github.com/user-attachments/assets/10e783b8-68ca-41e4-ae81-6ba4def58ce7" /> <img width="510" alt="image" src="https://github.com/user-attachments/assets/142f4d8e-715c-4419-93c8-e6a1fcddc7d1" />




All agents are orchestrated using the [OpenAI Agents SDK](https://platform.openai.com/docs/assistants/overview), which provides a structured and extensible framework for building LLM-driven applications.

## Key Features

- 🧠 Multi-agent coordination via OpenAI Agents SDK
- 📈 Real-time financial data retrieval using API-based RAG
- 🗣️ Natural language interface for user queries
- 📊 Data visualization with Plotly
- 🧪 Built with Streamlit for fast prototyping

---

## Tech Stack

- [OpenAI Agents SDK](https://platform.openai.com/docs/assistants/overview)
- [OpenAI API](https://platform.openai.com/)
- [Sectors.app API](https://sectors.app)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)

  ---

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/miqbalrp/agentic-ai.git
   cd agentic-ai
2. **Set up your environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. **Configure your environment variables**
   Create a .env file with:
   ```bash
   OPENAI_API_KEY=your_openai_key_here
   SECTORS_API_KEY=your_sectors_app_key_here
4. **Run the app**
   ```bash
   streamlit run app.py

## Inspiration
This project was inspired by the Agentic Patterns Workshop organized by Supertype. The hands-on session introduced practical techniques for building agent-based applications using modern LLMs and retrieval-augmented generation (RAG). The workshop and its accompanying course material — available at sectors.app/bulletin/agentic-patterns — provided the foundational ideas that sparked the development of this financial analytics app. 

## Learning Milestone
1. [2025-06-09] For the first version of the app, I have implement some of the fundamental concept on Multi-Agent System development:
   - **Tool-Use, Function Calling, and API-based RAG**: I implement `function_tool` decorator from Agent SDK framework to make API calls. The data of IDX stock that used in this app is the actual data, retrieved from Sectors.app API. This prevents the model halucinate with their own data training and provide wrong information.
   - **The Handoff and Delegation Pattern**: To orchestrate which Agent that should answer the query of user, I create `triage_agent` that responsible to understand the query of the user and handing off to the right agent.
   - **Data Validation with Pydantic**: During the development of this app, I learn that although AI is powerful on doing the task, we should put an extra care for the data output to make sure the orchestration is running smoothly. Hence, I try to standardize the output of each Agent using Pydantic so it will be displayed correctly on Streamlit. 
   - **Combining Text and Visualization in a Report**: If trend analysis and top companies agent are being called, they will provide the analysis as well as the supporting interactive visualization using Plotly Express. To make this happen, a strict data validation need to be implemented as mentioned in the previous point.
2. [2025-06-12] The main change in app_v2 is we are utilizing **agent-as-tool** concept (in `orchestrator_agent.py`) rather than handoffs (in `triage_agent.py`). The advantage of this is we able to make more than 1 agent work together rather than handing off to one of the agent. For instance, if the query asks summary overview of a company AND the trend analysis of daily closing price, then two agents will work together; `company_overview_agent` and `trend_analysis_agent`, orchestrated by `orchestrator_agent`. 
   


---
*This project is part of my ongoing journey into practical Agentic AI — suggestions and contributions are welcome!*
