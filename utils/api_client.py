import os
import json
import requests
from dotenv import load_dotenv

import streamlit as st

import logging
logger = logging.getLogger(__name__)

load_dotenv()
SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")

headers = {"Authorization": SECTORS_API_KEY}

def retrieve_from_endpoint(url: str) -> dict:
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Data retrieved successfully from {url}")
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
        raise SystemExit(err)
    return json.dumps(data)