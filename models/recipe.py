from . import db
from sqlalchemy import ForeignKey

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.relationship(
        'Ingredient', backref=db.backref('recipes', lazy='dynamic')
    )
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Recipe %r>' % self.title