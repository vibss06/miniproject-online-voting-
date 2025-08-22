from flask import Blueprint, request, jsonify
from models import db, Voter

bp = Blueprint("bp", __name__)

# Signup route
@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    voter = Voter(
        name=data["name"],
        email=data["email"],
        username=data["username"],
        password=data["password"],
    )
    db.session.add(voter)
    db.session.commit()
    return jsonify({"message": "Signup successful"}), 201


# Health check route (to test server is alive)
@bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})
