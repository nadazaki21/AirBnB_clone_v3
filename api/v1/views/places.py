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











# @app_views.route("/places_search", strict_slashes=False, methods=["POST"])
# def places_search():
#     """searches for places"""
#     if not request.is_json:
#         abort(400, description="Not a JSON")
#     data = request.get_json()
    
#     # If JSON body is empty, return all places
#     if not data:
#         places = storage.all(Place).values()
#         list_places = [place.to_dict() for place in places]
#         return jsonify(list_places)
    
#     states = data.get("states", [])
#     cities = data.get("cities", [])
#     amenities = data.get("amenities", [])

#     places = set()

#     # If states list is not empty
#     if states:
#         for state_id in states:
#             state = storage.get(State, state_id)
#             if state:
#                 for city in state.cities:
#                     for place in city.places:
#                         places.add(place)
    
#     # If cities list is not empty
#     if cities:
#         for city_id in cities:
#             city = storage.get(City, city_id)
#             if city:
#                 for place in city.places:
#                     places.add(place)
    
#     # Convert places set to list of dictionaries
#     places = list(places)
#     list_places = [place.to_dict() for place in places]

#     # If amenities list is not empty
#     if amenities:
#         final_places = []
#         for place in places:
#             place_amenities = [amenity.id for amenity in place.amenities]
#             if all(amenity in place_amenities for amenity in amenities):
#                 final_places.append(place.to_dict())
#         return jsonify(final_places)

#     return jsonify(list_places)