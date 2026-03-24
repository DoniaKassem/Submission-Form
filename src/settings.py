from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "weather.sqlite3"

WEATHER_LOCATION = {
    "name": "Boulder, CO",
    "latitude": 40.015,
    "longitude": -105.2705,
}

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH.as_posix()}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

