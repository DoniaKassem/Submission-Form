import requests

from .settings import WEATHER_LOCATION


def fetch_current_temperature() -> float:
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": WEATHER_LOCATION["latitude"],
            "longitude": WEATHER_LOCATION["longitude"],
            "current": "temperature_2m",
            "temperature_unit": "celsius",
        },
        timeout=15,
    )
    response.raise_for_status()

    payload = response.json()
    return float(payload["current"]["temperature_2m"])

