from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets
from datetime import datetime
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Recipe(db.Model):
    id = db.Column(db.String, primary_key = True, nullable=False)
    recipeid = db.Column(db.String, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(300))
    servings = db.Column(db.Integer)
    ready_in_min = db.Column(db.Integer)
    source_url = db.Column(db.String(300))
    num_likes = db.Column(db.Integer)
    cuisine = db.Column(db.String(100))
    summary = db.Column(db.String(5000))
    token = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, recipeid, title, image_url, servings, ready_in_min, source_url, num_likes, cuisine, summary, token,):
        self.id = self.set_id()
        self.recipeid = recipeid
        self.title = title
        self.image_url = image_url
        self.servings = servings
        self.ready_in_min = ready_in_min
        self.source_url = source_url
        self.num_likes = num_likes
        self.cuisine = cuisine
        self.summary = summary
        self.token = token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"Recipe #{self.id} {self.title} has been added to the database"

class RecipeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'recipeid', 'title', 'image_url', 'servings', 'ready_in_min', 'source_url', 'num_likes', 'cuisine', 'summary', 'token']

recipe_schema = RecipeSchema()
recipes_schemas = RecipeSchema(many=True)
