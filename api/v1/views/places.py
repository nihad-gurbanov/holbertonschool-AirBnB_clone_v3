#!/usr/bin/python3
""" Places module """

from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places/',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/places/<place_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places(city_id=None, place_id=None):
    """Retrieve cities"""
    status_code = 200
    if request.method == 'POST':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        new_place = request.get_json(silent=True)
        if new_place is None:
            abort(400, "Not a JSON")
        elif "name" not in new_place:
            abort(400, "Missing name")
        elif "user_id" not in new_place:
            abort(400, "Missing user_id")
        user = storage.get(User, new_place['user_id'])
        if user is None:
            abort(404)
        new_place['city_id'] = city_id
        new_place['state_id'] = city.state_id
        new_place = Place(**new_place)
        new_place.save()
        place_id = new_place.id
        status_code = 201
    if place_id:
        response = storage.get(Place, place_id)
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
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)
