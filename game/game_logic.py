from ai.ai_interface import generate_ai_response

class Game:
    def __init__(self, player, update_story_callback):
        self.player = player
        self.story_context = "You are in a fantasy world with a mysterious plot."
        self.update_story_callback = update_story_callback
    
    def start_game(self):
        initial_text = (
            "You find yourself in a mystical land, surrounded by towering trees and strange sounds. "
            "A path winds into the darkness ahead, and you feel a sense of adventure stirring in you. "
            "You can choose to explore the path, investigate the sounds, or look around for any clues."
        )
        self.update_story_callback(initial_text)
        self.story_context = initial_text

    def process_choice(self, player_input):
        prompt = f"{self.story_context}\nPlayer action: {player_input}\nResponse:"
        
        if "amulet" in self.player.inventory:
            prompt += " The player holds a mysterious glowing amulet."
        if self.player.reputation > 10:
            prompt += " The player is known as a hero in the nearby villages."
        
        response = generate_ai_response(prompt)
        
        # Update the story context and display response
        self.update_story_callback("\n" + response)
        self.story_context += f"\n{player_input}: {response}"

    def generate_next_story_part(self):
        """Generate the next part of the story without user input."""
        prompt = f"{self.story_context}\nContinue the story:"
        
        response = generate_ai_response(prompt)
        
        # Update the story context and display the generated response
        self.update_story_callback("\n" + response)
        self.story_context += f"\nAI: {response}"

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = ["amulet"]
        self.reputation = 15
