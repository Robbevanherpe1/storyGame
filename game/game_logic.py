from ai.ai_behavior import generate_response_with_player_context, generate_next_story_part
from data.story_content import initial_story_context, initial_text

class Game:
    def __init__(self, player, update_story_callback):
        self.player = player
        self.story_context = initial_story_context
        self.update_story_callback = update_story_callback

    def start_game(self):
        self.update_story_callback(initial_text)
        self.story_context = initial_text

    def process_choice(self, player_input):
        response = generate_response_with_player_context(self.story_context, player_input, self.player)
        
        # Update the story context and display response
        self.update_story_callback("\n" + response)
        self.story_context += f"\n{player_input}: {response}"

    def generate_next_story_part(self):
        response = generate_next_story_part(self.story_context)
        
        # Update the story context and display the generated response
        self.update_story_callback("\n" + response)
        self.story_context += f"\nAI: {response}"

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = ["amulet"]
        self.reputation = 15
