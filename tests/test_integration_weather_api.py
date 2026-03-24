import unittest
from datetime import datetime, timezone

from sqlalchemy.pool import StaticPool

from src.extensions import db
from src.models import WeatherReading
from src.web_app import create_app


class WeatherApiIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "SQLALCHEMY_ENGINE_OPTIONS": {
                    "connect_args": {"check_same_thread": False},
                    "poolclass": StaticPool,
                },
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            db.session.add(
                WeatherReading(
                    location="Boulder, CO",
                    temperature_c=18.5,
                    collected_at=datetime(2026, 3, 24, 21, 30, tzinfo=timezone.utc),
                )
            )
            db.session.commit()

    def tearDown(self) -> None:
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_weather_readings_endpoint_returns_stored_data(self) -> None:
        response = self.client.get("/api/weather-readings")

        self.assertEqual(response.status_code, 200)

        payload = response.get_json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["location"], "Boulder, CO")
        self.assertEqual(payload[0]["temperature_c"], 18.5)
        self.assertEqual(payload[0]["collected_at"], "2026-03-24T21:30:00")


if __name__ == "__main__":
    unittest.main()
