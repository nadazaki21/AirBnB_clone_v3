#!/usr/bin/python3
"""
Create a new view for State objects that
handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("states/", methods="GET", strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects: GET /api/v1/states
    """

    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route("states/<state_id>", strict_slashes=False)
def retive_state(STATE_ID):
    """Retrieves a State object: GET /api/v1/states/<state_id>
    """
    state = storage.get(State, STATE_ID)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("states/<state_id>", methods="DELETE", strict_slashes=False)
def delete_state(STATE_ID):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>
    """
    state = storage.get(State, STATE_ID)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("states/", methods="POST", strict_slashes=False)
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


@app_views.route("states/<state_id>", methods="PUT", strict_slashes=False)
def update_state(STATE_ID):
    """Updates a State object: PUT /api/v1/states/<state_id>
    """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")

    state = storage.get(State, STATE_ID)
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
