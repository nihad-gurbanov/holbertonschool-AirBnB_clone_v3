#!/usr/bin/python3
""" Users module """

from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users(user_id=None):
    """Retrieve users"""
    status_code = 200
    if request.method == 'POST':
        new_user = request.get_json(silent=True)
        if new_user is None:
            abort(400, "Not a JSON")
        elif "email" not in new_user:
            abort(400, "Missing email")
        elif "password" not in new_user:
            abort(400, "Missing password")
        new_user = User(**new_user)
        new_user.save()
        user_id = new_user.id
        status_code = 201
    if user_id:
        response = storage.get(User, user_id)
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
    users = []
    for key, user in storage.all("User").items():
        users.append(user.to_dict())
    return jsonify(users)
