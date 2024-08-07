#!/usr/bin/python3
""" Web route to handle all default RestFul API actions for Places """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Places of a City
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place Object
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    data["city_id"] = city_id

    new_place = Place(**data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)

    storage.save()

    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data:
        states = data.get('states')
        cities = data.get('cities')
        amenities = data.get('amenities')

    if not data or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]

        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
