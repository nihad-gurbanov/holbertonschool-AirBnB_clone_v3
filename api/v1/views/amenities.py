#!/usr/bin/python3
""" Amenities module """

from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities(amenity_id=None):
    """Retrieve amenities"""
    status_code = 200
    if request.method == 'POST':
        new_amenity = request.get_json(silent=True)
        if new_amenity is None:
            abort(400, "Not a JSON")
        elif "name" not in new_amenity:
            abort(400, "Missing name")
        new_amenity = Amenity(**new_amenity)
        new_amenity.save()
        amenity_id = new_amenity.id
        status_code = 201
    if amenity_id:
        response = storage.get(Amenity, amenity_id)
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
    amenities = []
    for key, amenity in storage.all("Amenity").items():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)
