#!/usr/bin/python3
""" City View """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=["GET"])
def return_places_of_cities(city_id):
    """views all places of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def return_place(place_id):
    """views a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """deleetes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=["POST"])
def create_place(city_id):
    """creates a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
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
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()

    for key, value in data.items():
        if key in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            pass
        else:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", strict_slashes=False, methods=["POST"])
def places_search():
    # If the HTTP request body is not valid JSON
    guide = request.get_json()
    if not guide:
        abort(400, "Not a JSON")

    state_ids = guide.get("states")
    city_ids = guide.get("cities")
    amenity_ids = guide.get("amenities")
    result = []

    # If the JSON body is empty or each list of all keys are empty:
    # retrieve all Place objects
    if not guide and not state_ids and not city_ids:
        result = storage.all(Place)

    # If states list is not empty, results should
    # include all Place objects for each State id listed
    if state_ids:
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        result.append(place)

    # If cities list is not empty, results should
    # include all Place objects for each City id listed
    if city_ids:
        for city_id in city_ids:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in result:
                        result.append(place)

    # If amenities list is not empty, limit search results to
    # only Place objects having all Amenity ids listed
    if amenity_ids:
        for place in result:
            if place.amenities:
                place_amenity_ids = [amenity.id for amenity in place.amenities]
                for amenity_id in amenity_ids:
                    if amenity_id not in place_amenity_ids:
                        result.remove(place)
                        break

    # serialize to json
    result = [storage.get(Place, place.id).to_dict() for place in result]
    
    return jsonify(result)