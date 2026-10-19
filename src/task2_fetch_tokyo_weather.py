import requests
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_weather_data() -> Dict[str, Any]:
    """
    Fetch the maximum temperature forecast for Tokyo using the Open-Meteo API.

    Returns:
        dict: A dictionary containing the date and the maximum temperature.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
        KeyError: If the expected data is not in the API response.
    """
    url = ("https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917"
           "&daily=temperature_2m_max&timezone=Asia/Tokyo")
    
    # Дата прогнозу визначається за часом Токіо (UTC+9).
    tomorrow = (datetime.now(timezone(timedelta(hours=9))) + timedelta(days=1)).date().isoformat()
    response = requests.get(url, params={"start_date": tomorrow, "end_date": tomorrow}, timeout=30)
    response.raise_for_status()
    daily = response.json()['daily']
    if not daily['time'] or not daily['temperature_2m_max']:
        raise ValueError("The API returned no daily temperature forecast.")
    temperature = daily['temperature_2m_max'][0]
    if temperature is None:
        raise ValueError("The API returned a missing temperature.")
    return {"date": daily['time'][0], "max_temperature": temperature}


if __name__ == "__main__":
    try:
        weather_data = fetch_weather_data()

        save_to_json(weather_data, "tokyo_weather.json")

        print("Data successfully saved to tokyo_weather.json")
    except Exception as e:
        raise SystemExit(f"An error occurred: {e}")
