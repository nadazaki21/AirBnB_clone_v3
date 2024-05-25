#!/usr/bin/python3
"""
Create a new view for State objects that
handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("states/", strict_slashes=False, methods=["GET"])
def all_states():
    """Retrieves the list of all State objects: GET /api/v1/states
    """

    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route("states/<state_id>", strict_slashes=False, methods=["GET"])
def retive_state(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("states/", strict_slashes=False, methods=["POST"])
def create_state():
    """Creates a State: POST /api/v1/states
    """

    if request.content_type != "application/json":
        abort(400, "Not a JSON")

    if not request.get_json():
        abort(400, "Not a JSON")

    kwargs = request.get_json()

    if "name" not in kwargs:
        abort(400, "Missing name")

    new_state = State(**kwargs)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>
    """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
