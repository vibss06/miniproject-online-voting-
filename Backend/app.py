from flask import Flask
from flask_cors import CORS
from models import db
from routes import bp as routes_bp

def create_app():
    app = Flask(__name__)

    # SQLite DB in this folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init DB
    db.init_app(app)

    # CORS for frontend on a different origin
    CORS(app)

    # Register API routes
    app.register_blueprint(routes_bp)

    # Create tables once
    with app.app_context():
        db.create_all()

    return app

# Expose `app` for gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
