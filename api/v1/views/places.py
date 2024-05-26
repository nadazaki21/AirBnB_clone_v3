#!/usr/bin/python3
""" City View """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
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
    """searches for places"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    final_list = []
    if data == {}:
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)

    elif "states" in data and data["states"] != []:
        for state in data["states"]:
            for city in storage.all(City).values():
                if "city" in data and data["city"] != []:
                    if city.state_id == state or city.id in data["cities"]:
                        for place in storage.all(Place).values():
                            if place.city_id == city.id:
                                final_list.append(place.to_dict())
                else:
                    if city.state_id == state:
                        for place in storage.all(Place).values():
                            if place.city_id == city.id:
                                final_list.append(place.to_dict())

        if "amenities" in data and data["amenities"] != []:
            for item in final_list:
                for amenity in item.amenities:
                    if amenity.id not in data["amenities"]:
                        final_list.remove(item)

    elif "cities" in data and data["cities"] != []:
        for city in data["cities"]:
            for place in storage.all(Place).values():
                if place.city_id == city:
                    final_list.append(place.to_dict())

        if "amenities" in data and data["amenities"] != []:
            for item in final_list:
                for amenity in item.amenities:
                    if amenity.id not in data["amenities"]:
                        final_list.remove(item)

    else:
        for place in storage.all(Place).values():
            final_list.append(place.to_dict())

        for item in final_list:
            for amenity in item.amenities:
                if amenity.id not in data["amenities"]:
                    final_list.remove(item)

    return jsonify(final_list)
