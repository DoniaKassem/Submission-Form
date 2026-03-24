# Flask Course Starter

This starter matches the "Setting up a Web Application" exercise from your course.

## Local Setup

### PowerShell

```powershell
cd my_flask_app
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "src/app.py"
flask run
```

### Bash

```bash
cd my_flask_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=src/app.py
flask run
```

Open `http://127.0.0.1:5000/` in your browser.

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

After installing dependencies, you can update `requirements.txt` with:

```bash
pip freeze > requirements.txt
```

