#!/usr/bin/python3
""" Reviews module """

from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews/',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_reviews(place_id=None, review_id=None):
    """Retrieve places"""
    status_code = 200
    if request.method == 'POST':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        new_review = request.get_json(silent=True)
        if new_review is None:
            abort(400, "Not a JSON")
        elif "text" not in new_review:
            abort(400, "Missing text")
        elif "user_id" not in new_review:
            abort(400, "Missing user_id")
        user = storage.get(User, new_review['user_id'])
        if user is None:
            abort(404)
        new_review['place_id'] = place_id
        new_review = Review(**new_review)
        new_review.save()
        review_id = new_review.id
        status_code = 201
    if review_id:
        response = storage.get(Review, review_id)
        if response is None:
            abort(404)
        if request.method == 'DELETE':
            storage.delete(response)
            storage.save()
            return jsonify({})
        elif request.method == 'PUT':
            update_data = request.get_json(silent=True)
            if update_data is None:
                abort(400, "Not a JSON")
            for key, value in update_data.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(response, key, value)
            storage.save()
        return jsonify(response.to_dict()), status_code
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)
