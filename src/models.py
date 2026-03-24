from datetime import datetime, timezone

from .extensions import db


class WeatherReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collected_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    location = db.Column(db.String(120), nullable=False)
    temperature_c = db.Column(db.Float, nullable=False)

