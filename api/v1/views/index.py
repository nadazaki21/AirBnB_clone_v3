#!/usr/bin/python3
"""
Flask App
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes

@app_views.route('/status', strict_slashes=False)
def return_status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def return_stats():
    objects_perclass_count = {'amenity': 0, 'city': 0, 'place': 0, 'state': 0, 'user': 0}
    for key, value in zip(objects_perclass_count.keys(), classes.values()):
        objects_perclass_count[key] = storage.count(value)
    return (jsonify(objects_perclass_count))
