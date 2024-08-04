#!/usr/bin/python3
"""
Cities web route
"""

from flask import jsonify, abort, request
from models import storage
from models.city import City
from api.v1.views import app_views


# Retrieve city object(s)
@app_views.route('/cities', strict_slashes=False)
@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id=None):
    """Retrieve city object(s)"""
    if not city_id:
        cities = storage.all(City)
        city_list = [city.to_dict() for city in cities.values()]

        return jsonify(city_list)

    else:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        return jsonify(city.to_dict())

# Deletes city object
@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return jsonify({})

# Creates a city object
@app_views.route('/cities', methods=["POST"], strict_slashes=False)
def create_city():
    """Creates new city object"""
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_city = City(**data)
    new_city.save()

    return jsonify(new_city.to_dict()), 201

# Updates a city object
@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    storage.save()

    return jsonify(city.to_dict())
