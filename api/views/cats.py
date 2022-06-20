from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.cat import Cat

cats = Blueprint('cats', 'cats')

@cats.route('/', methods=["POST"])
@login_required
def create():
  # parse incoming json request and store in data variable
  data = request.get_json()
  # retrieve user's profile data with read_token middleware function, assign to profile
  profile = read_token(request)
  # add profile_id property to data (ie req.body in Express)
  data["profile_id"] = profile["id"]
  # pass updated data dictionary to Cat model, which creates the new resource in our db.
  cat = Cat(**data)
  # add and commit changes to our db
  db.session.add(cat)
  db.session.commit()
  # return json response with new created cat data and 201 status code
  return jsonify(cat.serialize()), 201

@cats.route('/<id>', methods=["GET"])
def show(id):
  cat = Cat.query.filter_by(id=id).first()
  cat_data = cat.serialize()
  return jsonify(cat=cat_data), 200

@cats.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  cat = Cat.query.filter_by(id=id).first()

  if cat.profile_id != profile["id"]:
    return 'Forbidden', 403
  
  for key in data:
    setattr(cat, key, data[key])

  db.session.commit()
  return jsonify(cat.serialize()), 200