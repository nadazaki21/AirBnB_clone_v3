#!/usr/bin/python3
""" City View """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
import json


@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=["GET"])
def return_places_of_cities(city_id):
    """views all places of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return json.dumps(place_list, indent=2) + "\n"


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def return_place(place_id):
    """views a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return json.dumps(place.to_dict(), indent=2) + "\n"


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """deleetes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return {}, 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=["POST"])
def create_place(city_id):
    """creates a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    if "name" not in data:
        abort(400, description="Missing name")

    data["city_id"] = city_id

    place = Place(**data)
    storage.new(place)
    storage.save()
    return json.dumps(place.to_dict(), indent=2), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_city(place_id):
    """updates a city"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            pass
        else:
            setattr(place, key, value)

    storage.save()
    return json.dumps(place.to_dict(), indent=2) + "\n", 200
