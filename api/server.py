# server.py
import os
from flask import Flask, request, jsonify
from game.game_logic import Game, Player
from ai.ai_interface import generate_ai_response

app = Flask(__name__)

# Initialize a single game instance for simplicity
player = Player("Hero")
game = Game(player, lambda text: text)  # Provide a simple callback

@app.route("/start", methods=["GET"])
def start_game():
    game.start_game()
    return jsonify({"story": "Game started!"})

@app.route("/process", methods=["POST"])
def process_choice():
    user_input = request.json.get("choice", "")
    response = game.process_choice(user_input)
    return jsonify({"response": response})

@app.route("/continue", methods=["GET"])
def continue_story():
    response = generate_ai_response("Continue the story")
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
