from flask import Flask, request, jsonify, render_template, redirect, url_for

from models import db, Recipe, User  # Adjust imports based on your models.py
from app import app  # Assuming your Flask app is initialized in app.py

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Get all recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes])

# Get a single recipe by ID
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())

# Add a new recipe
@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    new_recipe = Recipe(
        name=data['name'],
        ingredients=data['ingredients'],
        instructions=data['instructions']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201

# Update a recipe
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.json
    recipe.name = data.get('name', recipe.name)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.instructions = data.get('instructions', recipe.instructions)
    db.session.commit()
    return jsonify(recipe.to_dict())

# Delete a recipe
@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted successfully'})

# User registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']  # Ensure you hash passwords in production
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# User login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:  # Replace with hashed password check
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

#Reviews and ratings
@app.route('/recipes/<int:recipe_id>/reviews', methods=['POST'])
def add_review(recipe_id):
    data = request.json
    recipe = Recipe.query.get_or_404(recipe_id)
    review = Review(
        content=data['content'],
        recipe_id=recipe.id,
        user_id=data['user_id']  # Assuming user ID is passed in the request
    )
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201

@app.route('/recipes/<int:recipe_id>/ratings', methods=['POST'])
def add_rating(recipe_id):
    data = request.json
    recipe = Recipe.query.get_or_404(recipe_id)
    rating = Rating(
        score=data['score'],
        recipe_id=recipe.id,
        user_id=data['user_id']  # Assuming user ID is passed in the request
    )
    db.session.add(rating)
    db.session.commit()
    return jsonify(rating.to_dict()), 201