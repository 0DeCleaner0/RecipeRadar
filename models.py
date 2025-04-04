from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for many-to-many relationship between Recipe and Ingredient
recipe_ingredient = db.Table(
    'recipe_ingredient',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    password_hash = db.Column(db.String(128))
    ingredients = db.Column(db.Text, nullable=True)  # Comma-separated list of ingredient names
    comments = db.relationship('Comment', backref='author', lazy=True)

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def remove_recipe(self, recipe):
        self.recipes.remove(recipe)

    def find_recipes(self):
        """Find recipes that can be made with the user's ingredients."""
        if not self.ingredients:
            return []
        user_ingredients = set(self.ingredients.split(','))
        return Recipe.query.filter(
            Recipe.ingredients.any(Ingredient.name.in_(user_ingredients))
        ).all()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.relationship(
        'Ingredient', secondary=recipe_ingredient, backref=db.backref('recipes', lazy='dynamic')
    )
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Recipe %r>' % self.title

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return '<Comment %r>' % self.content[:20]  # Show first 20 characters of the comment

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, score, recipe_id, user_id):
        self.score = score
        self.recipe_id = recipe_id
        self.user_id = user_id

    def __repr__(self):
        return '<Rating %r>' % self.score

    recipe = db.relationship('Recipe', backref=db.backref('ratings', lazy=True))
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))

def generate_password_hash(password):
    # Placeholder for password hashing logic
    return password  # In a real application, use a secure hashing algorithm

def check_password_hash(stored_password, provided_password):
    # Placeholder for password checking logic
    return stored_password == provided_password  # In a real application, use a secure comparison method

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Ingredient %r>' % self.name
