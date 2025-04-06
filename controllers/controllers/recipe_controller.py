from flask import Blueprint, request, jsonify
from models import db, Recipe

recipe_blueprint = Blueprint('recipe', __name__)

@recipe_blueprint.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@recipe_blueprint.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())

@recipe_blueprint.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    new_recipe = Recipe(
        title=data['title'],
        instructions=data['instructions']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201