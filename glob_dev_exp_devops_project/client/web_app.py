"""
1. The web interface will return the user name of a given user id stored inside
users table (please refer to Database section).

2. The user name of the user will be returned in an HTML format with a locator
to simplify testing.

3. In case the ID doesn't exist return an error (in HTML format)
"""

import os
from pathlib import Path
from typing import Any
import requests

from flask import Flask, redirect, render_template, request, url_for

from glob_dev_exp_devops_project.server.rest_app import (
    SERVER_RUN_HOST,
    SERVER_RUN_PORT,
)

# Flask connection details
CLIENT_RUN_HOST = os.environ.get("CLIENT_RUN_HOST", "127.0.0.1")
CLIENT_RUN_PORT = int(os.environ.get("CLIENT_RUN_PORT", 5001))
CLIENT_HTML_TEMPLATE_FOLDER = (
    Path(__file__).parent / ".." / ".." / "templates" / "client"
)
CLIENT_CSS_STATIC_FOLDER = Path(__file__).parent / ".." / ".." / "static"


# Flask app
def create_flask_app(
    template_folder: Path = Path(__file__).parent / "templates",
    static_folder: Path = Path(__file__).parent / "static",
):
    return Flask(
        import_name=__name__,
        template_folder=template_folder,
        static_folder=static_folder,
    )


web_app = create_flask_app(
    template_folder=CLIENT_HTML_TEMPLATE_FOLDER,
    static_folder=CLIENT_CSS_STATIC_FOLDER,
)

# How is the interaction between the frontend and the backend?
# The frontend will send a GET request to the backend with the user ID
# The backend will query the database and return the user name


@web_app.route("/get_user_data", methods=["GET"])
def get_user_data():
    if request.method == "GET":
        user_id = request.args.get("user_id")
        if user_id is None:
            return redirect(url_for("/"))
        elif not user_id.isdigit():
            return render_template("error.html", error="Invalid user ID")
        else:
            user_id = int(user_id)
        response = requests.get(
            f"http://{SERVER_RUN_HOST}:{SERVER_RUN_PORT}/users/{user_id}"
        )
        if response.status_code != 200:
            return render_template(
                "error.html", error="User ID not found in the database"
            )
        users: dict[str, Any] = response.json()
    return render_template("get_user_data.html", user_id=user_id, users=users)


@web_app.route("/")
@web_app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    web_app.run(host=CLIENT_RUN_HOST, port=CLIENT_RUN_PORT, debug=True)