from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -------------------------
# Voter model
# -------------------------
class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # (can hash later)

    def __repr__(self):
        return f"<Voter {self.username}>"


# -------------------------
# Candidate model
# -------------------------
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100), nullable=False)
    votes = db.relationship("Vote", backref="candidate", lazy=True)

    def __repr__(self):
        return f"<Candidate {self.name}>"


# -------------------------
# Vote model
# -------------------------
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey("voter.id"), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"), nullable=False)

    def __repr__(self):
        return f"<Vote Voter={self.voter_id} Candidate={self.candidate_id}>"
