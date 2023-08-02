#!/usr/bin/env python3

from models import db, Episode, Guest, Appearance
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class Episodes(Resource):
    def get(self):
        episodes = [episode.to_dict() for episode in Episode.query.all()]

        return make_response(
            episodes,
            200
        )
    
class EpisodeByID(Resource):
    def get(self, id):
        episode = Episode.query.filter_by(id = id).first().to_dict()

        if episode:
            return make_response(
                episode,
                200
            )
        else:
            return make_response(
                {
                    "error": "Episode not found"
                },
                404
            )
        
    def delete(self, id):
        episode = Episode.query.filter_by(id = id).first()

        if episode:
            for appearance in episode.appearances:
                db.session.delete(appearance)
                db.session.commit()

            db.session.delete(episode)
            db.session.commit()

            return make_response({}, 204)
        else:
            return make_response(
                {
                    "error": "Episode not found"
                }, 200
            )
        
class Guests(Resource):
    def get(self):
        guests = [guest.to_dict() for guest in Guest.query.all()]

        return make_response(guests, 200)
    
class Appearances(Resource):
    def get(self):
        appearances = [appearance.to_dict() for appearance in Appearance.query.all()]
        return make_response(appearances, 200)

    def post(self):
        new_appearance = Appearance(
            rating = request.form["rating"],
            episode_id = request.form["episode_id"],
            guest_id = request.form["guest_id"]
        )

        db.session.add(new_appearance)
        db.session.commit()

        new_appearance_dict = new_appearance.to_dict()

        return make_response(new_appearance_dict, 201)


api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeByID, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
