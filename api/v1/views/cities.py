#!/usr/bin/python3
""" City View """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request
import json 


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def return_cities_of_states(state_id):
    """ views all cities of a state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if state.id == state_id:
        city_list = []
        for city in state.cities:
            city_list.append(city.to_dict())
        return json.dumps(city_list, indent=2) +'\n'
    
@app_views.route('/cities/<city_id>', strict_slashes=False , methods=['GET'])
def return_city(city_id):
    """ views a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return json.dumps(city.to_dict(), indent=2) +'\n'  

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """ deleetes a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return {}, 200

@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """ creates a city """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    try:
        data = request.get_json()
        #print(f"data looks like {data}")
    except (Exception):
        abort(400, description="Not a JSON")

    if not 'name' in data:
        abort(400, description="Missing name")
        #return "Missing name", 400
    
    data["state_id"] = state_id
    
    city = City(**data)
    storage.new(city)
    storage.save()
    return json.dumps(city.to_dict(),indent=2), 201

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ updates a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    try:
        data = request.get_json()
    except (Exception):
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key in ['id', 'state_id', 'created_at', 'updated_at']:
            pass
        # else:
        #     setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
