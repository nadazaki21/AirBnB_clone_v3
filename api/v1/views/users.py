#!/usr/bin/python3
""" User view
"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(user).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def retive_user(user_id):
    """Retrieves a specific Amnity object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """Deletes a single  user object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """Creates an new user object"""

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Updates a user object: PUT /api/v1/users/<user_id>"""
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    user = storage.get(User, user_id)

    if user:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at", "email"]

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
