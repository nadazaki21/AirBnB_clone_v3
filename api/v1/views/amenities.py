#!/usr/bin/python3
""" Amenity View """
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    ameniies_list = []
    for amenity in amenities:
        ameniies_list.append(amenity.to_dict())

    return jsonify(ameniies_list)


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False,
    methods=["GET"])
def retive_amenity(amenity_id):
    """Retrieves a specific Amnity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False,
    methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes a single  Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """Creates an new Amenity object"""

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    "amenities/<amenity_id>", strict_slashes=False,
    methods=["PUT"])
def update_amenity(amenity_id):
    """Updates a amenity_id object"""
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
