#!/usr/bin/env python3

from .extensions import db
from .models import WeatherReading
from .settings import WEATHER_LOCATION
from .weather_service import fetch_current_temperature
from .web_app import create_app


def main() -> None:
    app = create_app()

    with app.app_context():
        current_temperature = fetch_current_temperature()
        reading = WeatherReading(
            location=WEATHER_LOCATION["name"],
            temperature_c=current_temperature,
        )
        db.session.add(reading)
        db.session.commit()

        print(
            f"Stored {reading.temperature_c:.1f}C for "
            f"{reading.location} at {reading.collected_at.isoformat()}"
        )


if __name__ == "__main__":
    main()

