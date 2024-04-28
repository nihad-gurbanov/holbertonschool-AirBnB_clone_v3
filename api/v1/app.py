#!/usr/bin/python3
"""Python script that starts a Flask web application"""


from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(e):
    """404 not found error case"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exc):
    """ShutDown current session on SQLAlchemy"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
