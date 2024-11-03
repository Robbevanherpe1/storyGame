from ai.ai_interface import generate_ai_response

def generate_response_with_player_context(story_context, player_input, player):
    prompt = f"{story_context}\nPlayer action: {player_input}\nResponse:"
    
    if "amulet" in player.inventory:
        prompt += " The player holds a mysterious glowing amulet."
    if player.reputation > 10:
        prompt += " The player is known as a hero in the nearby villages."
    
    response = generate_ai_response(prompt)
    return response

def generate_next_story_part(story_context):
    prompt = f"{story_context}\nContinue the story:"
    response = generate_ai_response(prompt)
    return response
