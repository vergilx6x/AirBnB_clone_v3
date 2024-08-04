#!/usr/bin/python3
"""
Reviews web route
"""
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieve a place reviews"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """Retrieve a review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>',
        methods=["DELETE"],
        strict_slashes=False
    )
def delete_review(review_id):
    """Deletes a review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({})


@app_views.route(
        '/places/<place_id>/reviews',
        methods=["POST"],
        strict_slashes=False
    )
def create_review(place_id):
    """Creates a new review for a place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    if not storage.get(User, data['user_id']):
        abort(404)

    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    data['place_id'] = place_id

    new_review = Review(**data)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>',
        methods=["PUT"],
        strict_slashes=False
    )
def update_review(review_id):
    """Updates a review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    storage.save()

    return jsonify(review.to_dict())
