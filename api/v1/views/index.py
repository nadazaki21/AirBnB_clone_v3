#!/usr/bin/python3
"""
Flask App
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes
import json


@app_views.route("/status", strict_slashes=False)
def return_status():
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
    return (json.dumps(objects_perclass_count, indent=2)) + "\n"
