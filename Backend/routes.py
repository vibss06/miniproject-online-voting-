from flask import Blueprint, request, jsonify
from models import db, Voter, Candidate, Vote

bp = Blueprint("routes", __name__)

@bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200

# ---------- Auth ----------
@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(force=True)
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    username = data.get("username", "").strip().lower()
    password = data.get("password", "").strip()

    if not all([name, email, username, password]):
        return jsonify({"error": "All fields are required"}), 400

    if Voter.query.filter((Voter.username == username) | (Voter.email == email)).first():
        return jsonify({"error": "User with this username/email already exists"}), 400

    voter = Voter(name=name, email=email, username=username, password=password)
    db.session.add(voter)
    db.session.commit()
    return jsonify({"message": "Signup successful", "voter_id": voter.id}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username", "").strip().lower()
    password = data.get("password", "").strip()
    voter = Voter.query.filter_by(username=username, password=password).first()
    if not voter:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({
        "message": "Login successful",
        "voter": {"id": voter.id, "name": voter.name, "username": voter.username}
    }), 200

# ---------- Candidates ----------
@bp.route("/candidates", methods=["GET"])
def get_candidates():
    candidates = Candidate.query.order_by(Candidate.name.asc()).all()
    return jsonify([{"id": c.id, "name": c.name, "party": c.party} for c in candidates]), 200

@bp.route("/candidates", methods=["POST"])
def add_candidate():
    data = request.get_json(force=True)
    name = data.get("name", "").strip()
    party = data.get("party", "").strip()
    if not name or not party:
        return jsonify({"error": "Name and party are required"}), 400
    c = Candidate(name=name, party=party)
    db.session.add(c)
    db.session.commit()
    return jsonify({"message": "Candidate added", "candidate_id": c.id}), 201

# ---------- Voting ----------
@bp.route("/vote", methods=["POST"])
def cast_vote():
    data = request.get_json(force=True)
    voter_id = data.get("voter_id")
    candidate_id = data.get("candidate_id")

    if not voter_id or not candidate_id:
        return jsonify({"error": "voter_id and candidate_id are required"}), 400

    if not Voter.query.get(voter_id):
        return jsonify({"error": "Voter not found"}), 404
    if not Candidate.query.get(candidate_id):
        return jsonify({"error": "Candidate not found"}), 404

    if Vote.query.filter_by(voter_id=voter_id).first():
        return jsonify({"error": "You have already voted"}), 400

    v = Vote(voter_id=voter_id, candidate_id=candidate_id)
    db.session.add(v)
    db.session.commit()
    return jsonify({"message": "Vote cast successfully"}), 201

# ---------- Results ----------
@bp.route("/results", methods=["GET"])
def results():
    # Return candidate-wise totals
    candidates = Candidate.query.all()
    counts = []
    for c in candidates:
        total = Vote.query.filter_by(candidate_id=c.id).count()
        counts.append({"id": c.id, "name": c.name, "party": c.party, "votes": total})
    return jsonify(counts), 200
