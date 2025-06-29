import os
import streamlit as st
from dotenv import load_dotenv
import logging

# Load .env variables if .env file exists
load_dotenv()  # This loads environment variables from .env into os.environ

logger = logging.getLogger(__name__)

def setup_openai_api_key():
    # Check if OPENAI_API_KEY is already set in environment (e.g., from .env)
    if os.getenv("OPENAI_API_KEY"):
        # Already set, do nothing or just confirm
        logger.info("OPENAI_API_KEY is already set in the environment.")
        pass
    elif "OPENAI_API_KEY" in st.secrets:
        logger.info("Setting OPENAI_API_KEY from Streamlit secrets.")
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    else:
        logger.error("OPENAI_API_KEY not found in .env or Streamlit secrets.")
        raise RuntimeError("OPENAI_API_KEY not found in .env or Streamlit secrets.")

def setup_sectors_api_key():
    if os.getenv("SECTORS_API_KEY"):
        logger.info("SECTORS_API_KEY is already set in the environment.")
        pass
    elif "SECTORS_API_KEY" in st.secrets:
        logger.info("Setting SECTORS_API_KEY from Streamlit secrets.")
        os.environ["SECTORS_API_KEY"] = st.secrets["SECTORS_API_KEY"]
    else:
        logger.error("SECTORS_API_KEY not found in .env or Streamlit secrets.") 
        raise RuntimeError("SECTORS_API_KEY not found in .env or Streamlit secrets.")
