#!/usr/bin/env python3

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


INDEX_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Flask Starter</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background: #f4f7fb;
        color: #1d2733;
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
      }
      main {
        width: min(560px, 92vw);
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 14px 40px rgba(31, 41, 55, 0.12);
      }
      h1 {
        margin-top: 0;
      }
      label {
        display: block;
        font-weight: bold;
        margin-bottom: 0.5rem;
      }
      input[type="text"] {
        width: 100%;
        box-sizing: border-box;
        padding: 0.85rem 1rem;
        border: 1px solid #c9d3df;
        border-radius: 8px;
        margin-bottom: 1rem;
      }
      button {
        background: #0b63ce;
        color: #ffffff;
        border: 0;
        border-radius: 8px;
        padding: 0.85rem 1.1rem;
        cursor: pointer;
      }
      a {
        color: #0b63ce;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>Flask Starter App</h1>
      <p>Enter text below and submit the form to see it echoed back.</p>
      <form action="/echo_user_input" method="POST">
        <label for="user_input">Your input</label>
        <input id="user_input" name="user_input" type="text" placeholder="Type something here">
        <button type="submit">Submit!</button>
      </form>
    </main>
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


@app.route("/")
def main():
    return INDEX_HTML


@app.route("/echo_user_input", methods=["POST"])
def echo_user_input():
    user_input = request.form.get("user_input", "").strip()
    return response_html(user_input)


if __name__ == "__main__":
    app.run(debug=True)
