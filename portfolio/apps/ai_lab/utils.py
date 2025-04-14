
import os
import re
import requests
from django.conf import settings


class StockAPI:
    BASE_URL = "https://www.alphavantage.co/query"

    @staticmethod
    def get_stock_price(symbol):
        api_key = settings.ALPHA_VANTAGE_API_KEY
        if not api_key:
            raise ValueError("Missing API key for Alpha Vantage")

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": api_key,
        }
        response = requests.get(StockAPI.BASE_URL, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"API error: {response.status_code}")

        data = response.json()
        price = data.get("Global Quote", {}).get("05. price", "Unknown")
        return {"symbol": symbol, "price": price}


def generate_file_name_with_extension(prompt, dir, extension):
    """
    Generate a unique file name with extension based on the prompt
    """
    # Convert the prompt to lowercase, replace spaces with underscores, and limit to 25 characters
    base_file_name = "_".join(prompt.lower().split())[:25]

    version = get_next_version_number(base_file_name, extension, dir)

    return f"{base_file_name}_v{version}.{extension}"


def get_next_version_number(base_file_name, extension, dir):
    """
    Determine the next version number for a file in the directory.
    """
    if not dir or not os.path.exists(dir):
        return 1

    file_pattern = re.compile(
        rf"^{re.escape(base_file_name)}_v(\d+)\.{re.escape(extension)}$"
    )
    highest_version = 0

    for file in os.listdir(dir):
        match = file_pattern.match(file)
        if match:
            file_version = int(match.group(1))
            if file_version > highest_version:
                highest_version = file_version

    return highest_version + 1
