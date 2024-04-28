#!/usr/bin/python3
""" States module """

from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states(state_id=None):
    """Retrieve states"""
    status_code = 200
    if request.method == 'POST':
        new_state = request.get_json(silent=True)
        if new_state is None:
            abort(400, "Not a JSON")
        elif "name" not in new_state:
            abort(400, "Missing name")
        new_state = State(**new_state)
        new_state.save()
        state_id = new_state.id
        status_code = 201
    if state_id:
        response = storage.get(State, state_id)
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
    states = []
    for key, state in storage.all("State").items():
        states.append(state.to_dict())
    return jsonify(states)
