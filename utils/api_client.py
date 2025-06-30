import os
import json
import requests
from utils.config import setup_sectors_api_key

import streamlit as st

import logging

setup_sectors_api_key()

logger = logging.getLogger(__name__)

SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")

headers = {"Authorization": SECTORS_API_KEY}

def retrieve_from_endpoint(url: str) -> dict:
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Data retrieved successfully from {url}")
        return data  
    except requests.exceptions.HTTPError as err:
        if err.response is not None:
            logger.error(f"HTTP error {err.response.status_code}: {err.response.text}")
            try:
                return err.response.json()
            except ValueError:
                # Response not JSON
                return {"error": err.response.text}
        else:
            logger.error(f"HTTP error occurred: {err}")
            return {"error": str(err)}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": str(e)}