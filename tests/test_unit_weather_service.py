import unittest
from unittest.mock import MagicMock, patch

from src.settings import WEATHER_LOCATION
from src.weather_service import fetch_current_temperature


class WeatherServiceUnitTest(unittest.TestCase):
    @patch("src.weather_service.requests.get")
    def test_fetch_current_temperature_returns_temperature_from_api_payload(
        self, mock_get: MagicMock
    ) -> None:
        fake_response = MagicMock()
        fake_response.json.return_value = {
            "current": {
                "temperature_2m": 12.7,
            }
        }
        mock_get.return_value = fake_response

        temperature = fetch_current_temperature()

        self.assertEqual(temperature, 12.7)
        mock_get.assert_called_once_with(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": WEATHER_LOCATION["latitude"],
                "longitude": WEATHER_LOCATION["longitude"],
                "current": "temperature_2m",
                "temperature_unit": "celsius",
            },
            timeout=15,
        )
        fake_response.raise_for_status.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
