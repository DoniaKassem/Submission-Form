# Flask Course Starter

This starter matches the "Setting up a Web Application" exercise from your course.

## Local Setup

### PowerShell

```powershell
cd my_flask_app
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "src.app"
flask run
```

### Bash

```bash
cd my_flask_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=src.app
flask run
```

Open `http://127.0.0.1:5000/` in your browser.

## Data Collection

This project now includes a separate data collector process that fetches the
current temperature for Boulder, Colorado and stores it in SQLite.

Run it manually with:

```powershell
python -m src.collector
```

Each run inserts a new row into `weather.sqlite3`, and the web app shows the
latest readings on the homepage. The recent readings are also exposed as JSON
at `/api/weather-readings`.

## Tests

Run the automated tests with:

```powershell
python -m unittest discover -s tests -v
```

The project includes:

- a unit test for the weather API parsing logic
- an integration test for the Flask `/api/weather-readings` endpoint

## Git Setup

```bash
git init
git add .
git commit -m "First commit"
git branch -M main
git remote add origin <remote_url>
git push -u origin main
```

## Heroku Files

This project already includes:

- `requirements.txt`
- `Procfile`

The `Procfile` now defines both:

- `web: gunicorn src.app:app`
- `collector: python -m src.collector`

After installing dependencies, you can update `requirements.txt` with:

```bash
pip freeze > requirements.txt
```
