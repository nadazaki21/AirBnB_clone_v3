#!/usr/bin/python3
""" City View """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route(
    "/cities/<city_id>/places",
    strict_slashes=False, methods=["GET"])
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


@app_views.route(
    "/places/<place_id>",
    strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """deleetes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places",
    strict_slashes=False, methods=["POST"])
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
    """searches for places"""
    if request.content_type != "application/json":
        abort(400, description="Not a JSON")
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data:
        states = data.get("states")
        cities = data.get("cities")
        amenities = data.get("amenities")

    if not (states or cities or amenities):
        places = storage.all(Place).values()
        places_list = [place.to_dict() for place in places]
        return jsonify(places_list)
    places_list = []

    if states:
        states_obj = [storage.get(State, state_id) for state_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.palces:
                            places_list.append(place)

    if cities:
        cities_obj = [storage.get(City, city_id) for city_id in cities]
        for city in cities_obj:
            if city:
                for place in city.places:
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            all_palces = storage.all(Place).values()
            amenities_obj = [storage.get(Amenity, am_id)
                             for am_id in amenities]
            for place in all_palces:
                if all([my_amenity in place.amenities
                        for my_amenity in amenities_obj]):
                    places_list.append(place)

    places = []
    for places_obj in places_list:
        places_dict = places_obj.to_dict()
        places_dict.pop("amenities", None)
        places.append(places_dict)
    return jsonify(places)
