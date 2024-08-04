#!/usr/bin/python3
"""
Flask api application implementation
"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Cleans up resources after each request"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles 404 - not found error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))

    app.run(host=host, port=port, threaded=True)
