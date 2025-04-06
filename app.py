from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from controllers import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    register_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)