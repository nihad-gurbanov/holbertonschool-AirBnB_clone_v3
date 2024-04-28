#!/usr/bin/python3
""" Cities module """

from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities/',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/cities/<city_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
def cities(state_id=None, city_id=None):
    """Retrieve states"""
    status_code = 200
    if request.method == 'POST':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        new_city = request.get_json(silent=True)
        if new_city is None:
            abort(400, "Not a JSON")
        elif "name" not in new_city:
            abort(400, "Missing name")
        new_city['state_id'] = state_id
        new_city = City(**new_city)
        new_city.save()
        city_id = new_city.id
        status_code = 201
    if city_id:
        response = storage.get(City, city_id)
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
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)
