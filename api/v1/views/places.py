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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending
    of the JSON in the body of the request
    """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")

    req = request.get_json()
    if req is None or (
        req.get('states') is None and
        req.get('cities') is None and
        req.get('amenities') is None
    ):
        obj_places = storage.all(Place)
        return jsonify([obj.to_dict() for obj in obj_places.values()])

    places = set()

    if req.get('states'):
        obj_states = {storage.get(State, id) for id in req.get('states')}

        for obj_state in obj_states:
            for obj_city in obj_state.cities:
                for obj_place in obj_city.places:
                    places.add(obj_place)

    if req.get('cities'):
        obj_cities = {storage.get(City, id) for id in req.get('cities')}
        obj_cities.discard(None)
        for obj_city in obj_cities:
            for obj_place in obj_city.places:
                places.add(obj_place)

    if not places:
        places = storage.all(Place).values()

    if req.get('amenities'):
        obj_am = [storage.get(Amenity, id) for id in req.get('amenities')]
        conf_places = []
        for place in places:
            conf_places.append(place)
            amenities = place.amenities
            for amenity in obj_am:
                if amenity not in amenities:
                    conf_places.pop(-1)
                    break
        places = conf_places
    places = [obj.to_dict() for obj in places]
    return jsonify(places)
