#!/usr/bin/python3
""" script that defines a Flask blueprint resources"""


from api.v1.views import app_views, storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities(amenity_id=None):
    """Retrieves the list of all Amenity objects or one Amenity"""
    amenity_dict = storage.all("Amenity")
    if amenity_id is None:
        amenities_list = []
        for obj in amenity_dict.values():
            amenities_list.append(obj.to_dict())
        return jsonify(amenities_list)
    try:
        return jsonify(amenity_dict[f"Amenity.{amenity_id}"].to_dict())
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenities(amenity_id):
    """Deletes Amenity object"""
    amenity_dict = storage.all("Amenity")
    try:
        storage.delete(amenity_dict[f"Amenity.{amenity_id}"])
        storage.save()
        return jsonify({})
    except Exception:
        abort(404)


@app_views.route('/amenities/', methods=['POST'])
def add_amenities():
    """Adds Amenity object"""
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    try:
        name = http_dic["name"]
    except KeyError:
        abort(400, 'Missing name')
    new_amenity = Amenity(**http_dic)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def edit_amenities(amenity_id):
    """Edits Amenity object"""
    amenity_dict = storage.all("Amenity")
    try:
        amenity = amenity_dict[f"Amenity.{amenity_id}"]
    except KeyError:
        abort(404)
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for key, value in http_dic.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
