#!/usr/bin/python3
""" City View """
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
import json


@app_views.route("/places/<place_id>/reviews", strict_slashes=False, methods=["GET"])
def return_reviews_of_places(place_id):
    """views all reviws of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    # if place.id == place_id:  # diff 1
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return json.dumps(reviews_list, indent=2) + "\n"


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def return_review(review_id):
    """views a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    sorted_dict = dict(sorted(review.to_dict().items()))  # diff 2
    return json.dumps(sorted_dict, indent=2) + "\n"


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """deleetes a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return {}, 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False, methods=["POST"])
def create_review(place_id):
    """creates a review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    if "text" not in data:
        abort(400, description="Missing text")

    data["state_id"] = place_id

    review = Review(**data)
    storage.new(review)
    storage.save()
    return json.dumps(review.to_dict(), indent=2), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """updates a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            pass
        else:
            setattr(review, key, value)

    storage.save()
    return json.dumps(review.to_dict(), indent=2) + "\n"
