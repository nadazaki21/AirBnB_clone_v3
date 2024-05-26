#!/usr/bin/python3
""" Place amenity relation view"""

from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t
from flask import jsonify, abort, request
import json


@app_views.route(
    "/places/<place_id>/amenities",
    strict_slashes=False, methods=["GET"])
def return_amenities_of_place(place_id):
    """return all the amenities of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all_amenities = []
    if storage_t == "db":
        for amenity in place.amenities:
            all_amenities.append(amenity.to_dict())
    else:
        # print(place.amenity_ids)
        for id in place.amenity_ids:
            all_amenities.append(storage.get(Amenity, id).to_dict())
    return jsonify(all_amenities)
    # return json.dumps(all_amenities , indent=2) + "\n"


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    strict_slashes=False,
    methods=["DELETE"],
)
def delete_amenity_from_place(place_id, amenity_id):
    """deletes a amenity from a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if storage_t == "db":
        place.amenities.remove(amenity)
    else:
        print(place.amenity_ids)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    strict_slashes=False, methods=["POST"]
)
def add_amenity_to_place(place_id, amenity_id):
    """adds a amenity to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if storage_t == "db":
        place.amenities.append(amenity)
        storage.save()
    else:
        place.amenity_ids.append(amenity_id)
        storage.save()
    return jsonify(amenity.to_dict()), 201
