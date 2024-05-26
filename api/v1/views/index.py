#!/usr/bin/python3
"""this script to define app_views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes


@app_views.route('/status')
def view():
    """return json"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def return_stats():
    objects_perclass_count = {
        "amenities": 0,
        "cities": 0,
        "places": 0,
        "reviews": 0,
        "states": 0,
        "users": 0,
    }
    for key, value in zip(objects_perclass_count.keys(), classes.values()):
        objects_perclass_count[key] = storage.count(value)
    return jsonify(objects_perclass_count)
