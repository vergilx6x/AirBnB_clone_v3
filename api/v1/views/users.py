#!/usr/bin/python3
""" methods to handle all default RESTFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/users', strict_slashes=False)
@app_views.route('/users/<user_id>', strict_slashes=False)
def get_users(user_id=None):
    """ Retrieves a specific user """
    if not user_id:
        users = storage.all(User).values()
        list_users = [user.to_dict() for user in users]

        return jsonify(list_users)

    else:
        user = storage.get(User, user_id)
        if not user:
            abort(404)

        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400

    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400

    new_user = User(**data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)

    storage.save()

    return jsonify(user.to_dict())
