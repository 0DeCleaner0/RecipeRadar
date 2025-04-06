from .recipe_controller import recipe_blueprint
from .user_controller import user_blueprint
from .review_controller import review_blueprint

def register_blueprints(app):
    app.register_blueprint(recipe_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(review_blueprint)