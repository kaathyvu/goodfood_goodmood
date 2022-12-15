from flask import Blueprint, request, jsonify
from recipe_inventory.helpers import token_required
from recipe_inventory.models import db, Recipe, recipe_schema, recipes_schemas

api = Blueprint('api', __name__, url_prefix ='/api')

@api.route('/getdata')
def getdata():
    return {'some': 'value'}


# CREATE RECIPE
@api.route('/recipes', methods = ['POST'])
def create_recipe():
    recipeid = request.json['recipeid']
    title = request.json['title']
    image_url = request.json['image_url']
    servings = request.json['servings']
    ready_in_min = request.json['ready_in_min']
    source_url = request.json['source_url']
    num_likes = request.json['num_likes']
    cuisine = request.json['cuisine']
    summary = request.json['summary']
    token = request.json['token']

    print(f"User token: {token}")

    recipe = Recipe(recipeid, title, image_url, servings, ready_in_min, source_url, num_likes, cuisine, summary, token)
    db.session.add(recipe)
    db.session.commit()

    response = recipe_schema.dump(recipe)
    return jsonify(response)


# RETRIEVE ALL RECIPES
@api.route('/recipes/<token>', methods = ['GET'])
def get_recipes(token):
    recipes = Recipe.query.filter_by(token=token).all()
    response = recipes_schemas.dump(recipes)
    return jsonify(response)

# RETRIEVE ONE RECIPE
@api.route('/recipes/<token>/<id>', methods=['GET'])
def get_recipe(token, id):
    owner = token
    if owner == token:
        recipe = Recipe.query.get(id)
        response = recipe_schema.dump(recipe)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


# UPDATE RECIPE
@api.route('/recipes/<token>/<id>', methods = ['POST', 'PUT'])
def update_recipe(token, id):
    recipe = Recipe.query.get(id)
    recipe.recipeid = request.json['recipeid']
    recipe.title = request.json['title']
    recipe.image_url = request.json['image_url']
    recipe.servings = request.json['servings']
    recipe.ready_in_min = request.json['ready_in_min']
    recipe.source_url = request.json['source_url']
    recipe.num_likes = request.json['num_likes']
    recipe.cuisine = request.json['cuisine']
    recipe.summary = request.json['summary']
    recipe.token = token

    db.session.commit()
    response = recipe_schema.dump(recipe)
    return jsonify(response)

# DELETE RECIPE
@api.route('/recipes/<token>/<id>', methods = ['DELETE'])
def delete_recipe(token, id):
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    response = recipe_schema.dump(recipe)
    return jsonify(response)