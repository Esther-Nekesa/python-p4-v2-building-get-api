from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# 1. GET all games
@app.route('/games')
def games():
    games_list = [game.to_dict() for game in Game.query.all()]
    return make_response(games_list, 200)

# 2. GET a single game by ID
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if not game:
        return make_response({"error": "Game not found"}, 404)
    
    return make_response(game.to_dict(), 200)

# 3. GET all users who reviewed a specific game (using Association Proxy)
@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if not game:
        return make_response({"error": "Game not found"}, 404)

    # Use the association proxy 'users' defined in the Game model
    users_list = [user.to_dict(rules=("-reviews",)) for user in game.users]
    return make_response(users_list, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)