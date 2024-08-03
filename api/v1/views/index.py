#!/usr/bin/python3
"""
Index page
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Returns status code in json"""
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats')
def stats():
    """Return the number of each object by type."""
    return jsonify(storage.count)
