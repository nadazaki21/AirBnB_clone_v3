#!/usr/bin/python3
""" script that defines a Flask blueprint resources"""


from api.v1.views import app_views, storage, User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id=None):
    """Retrieves the list of all User objects or one User"""
    user_dict = storage.all("User")
    if user_id is None:
        users_list = []
        for obj in user_dict.values():
            users_list.append(obj.to_dict())
        return jsonify(users_list)
    try:
        return jsonify(user_dict[f"User.{user_id}"].to_dict())
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_users(user_id):
    """Deletes User object"""
    user_dict = storage.all("User")
    try:
        storage.delete(user_dict[f"User.{user_id}"])
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/users', methods=['POST'])
def add_users():
    """Adds User object"""
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    try:
        email = http_dic["email"]
    except KeyError:
        abort(400, 'Missing email')
    try:
        password = http_dic["password"]
    except KeyError:
        abort(400, 'Missing password')
    new_user = User(**http_dic)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def edit_users(user_id):
    """Edits User object"""
    user_dict = storage.all("User")
    try:
        user = user_dict[f"User.{user_id}"]
    except KeyError:
        abort(404)
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for key, value in http_dic.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
