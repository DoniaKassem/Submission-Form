from flask import Flask, jsonify, request
from markupsafe import escape

from .extensions import db
from .models import WeatherReading
from .settings import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    WEATHER_LOCATION,
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def main():
        latest_reading = (
            WeatherReading.query.order_by(WeatherReading.collected_at.desc()).first()
        )
        recent_readings = (
            WeatherReading.query.order_by(WeatherReading.collected_at.desc())
            .limit(5)
            .all()
        )
        return index_html(latest_reading, recent_readings)

    @app.route("/echo_user_input", methods=["POST"])
    def echo_user_input():
        user_input = request.form.get("user_input", "").strip()
        return response_html(user_input)

    @app.route("/api/weather-readings")
    def weather_readings():
        readings = (
            WeatherReading.query.order_by(WeatherReading.collected_at.desc())
            .limit(20)
            .all()
        )
        return jsonify(
            [
                {
                    "location": reading.location,
                    "temperature_c": reading.temperature_c,
                    "collected_at": reading.collected_at.isoformat(),
                }
                for reading in readings
            ]
        )

    return app


def index_html(latest_reading: WeatherReading | None, recent_readings: list[WeatherReading]) -> str:
    latest_temperature = "No data collected yet"
    latest_timestamp = "Run `python -m src.collector` to fetch the first reading."

    if latest_reading:
        latest_temperature = f"{latest_reading.temperature_c:.1f} C"
        latest_timestamp = latest_reading.collected_at.strftime("%Y-%m-%d %H:%M:%S UTC")

    recent_rows = "".join(
        (
            "<tr>"
            f"<td>{escape(reading.location)}</td>"
            f"<td>{reading.temperature_c:.1f} C</td>"
            f"<td>{reading.collected_at.strftime('%Y-%m-%d %H:%M:%S UTC')}</td>"
            "</tr>"
        )
        for reading in recent_readings
    )

    if not recent_rows:
        recent_rows = (
            "<tr>"
            "<td colspan='3'>No weather readings have been collected yet.</td>"
            "</tr>"
        )

    return f"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Flask Weather Collector</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background: #f4f7fb;
        color: #1d2733;
        margin: 0;
        padding: 2rem 1rem;
      }}
      .page {{
        width: min(960px, 100%);
        margin: 0 auto;
        display: grid;
        gap: 1.5rem;
      }}
      .card {{
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 14px 40px rgba(31, 41, 55, 0.12);
      }}
      h1, h2 {{
        margin-top: 0;
      }}
      .weather-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
      }}
      .weather-stat {{
        background: #eef5ff;
        border-radius: 10px;
        padding: 1rem;
      }}
      .weather-label {{
        font-size: 0.9rem;
        color: #526173;
      }}
      .weather-value {{
        font-size: 1.7rem;
        font-weight: bold;
        margin-top: 0.35rem;
      }}
      label {{
        display: block;
        font-weight: bold;
        margin-bottom: 0.5rem;
      }}
      input[type="text"] {{
        width: 100%;
        box-sizing: border-box;
        padding: 0.85rem 1rem;
        border: 1px solid #c9d3df;
        border-radius: 8px;
        margin-bottom: 1rem;
      }}
      button {{
        background: #0b63ce;
        color: #ffffff;
        border: 0;
        border-radius: 8px;
        padding: 0.85rem 1.1rem;
        cursor: pointer;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th, td {{
        text-align: left;
        padding: 0.8rem 0.6rem;
        border-bottom: 1px solid #e5edf6;
      }}
      code {{
        background: #f3f6fa;
        padding: 0.15rem 0.35rem;
        border-radius: 4px;
      }}
      a {{
        color: #0b63ce;
      }}
    </style>
  </head>
  <body>
    <div class="page">
      <section class="card">
        <h1>Weather Collection Demo</h1>
        <p>
          This web app now includes a separate data-collection process that fetches
          weather data for {escape(WEATHER_LOCATION["name"])} and stores it in SQLite.
        </p>
        <div class="weather-grid">
          <div class="weather-stat">
            <div class="weather-label">Latest temperature</div>
            <div class="weather-value">{latest_temperature}</div>
          </div>
          <div class="weather-stat">
            <div class="weather-label">Latest collection time</div>
            <div class="weather-value" style="font-size: 1rem;">{escape(latest_timestamp)}</div>
          </div>
        </div>
        <p>
          Run <code>python -m src.collector</code> whenever you want to collect
          another data point. JSON output is also available at
          <a href="/api/weather-readings">/api/weather-readings</a>.
        </p>
      </section>

      <section class="card">
        <h2>Submission Form</h2>
        <p>Enter text below and submit the form to see it echoed back.</p>
        <form action="/echo_user_input" method="POST">
          <label for="user_input">Your input</label>
          <input id="user_input" name="user_input" type="text" placeholder="Type something here">
          <button type="submit">Submit!</button>
        </form>
      </section>

      <section class="card">
        <h2>Recent Weather Readings</h2>
        <table>
          <thead>
            <tr>
              <th>Location</th>
              <th>Temperature</th>
              <th>Collected at</th>
            </tr>
          </thead>
          <tbody>
            {recent_rows}
          </tbody>
        </table>
      </section>
    </div>
  </body>
</html>
"""


def response_html(user_input: str) -> str:
    safe_input = escape(user_input) if user_input else "No input was provided."
    return f"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Submitted Input</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background: #f4f7fb;
        color: #1d2733;
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
      }}
      main {{
        width: min(560px, 92vw);
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 14px 40px rgba(31, 41, 55, 0.12);
      }}
      .result {{
        margin: 1rem 0;
        padding: 1rem;
        background: #eef5ff;
        border-radius: 8px;
      }}
      a {{
        color: #0b63ce;
      }}
    </style>
  </head>
  <body>
    <main>
      <h1>Submitted Input</h1>
      <div class="result">{safe_input}</div>
      <a href="/">Back to form</a>
    </main>
  </body>
</html>
"""
