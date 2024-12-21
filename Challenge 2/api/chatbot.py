from dotenv import load_dotenv
import os
from gemini import GeminiClient  # Hypothetical library; check actual API

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


# Initialize the Gemini client
gemini_client = GeminiClient(api_key=GEMINI_API_KEY)

def parse_recipes(file_path):
    with open(file_path, "r") as file:
        recipes = file.read().split("\n\n")
    
    parsed_recipes = []
    for recipe in recipes:
        lines = recipe.split("\n")
        parsed_recipes.append({
            "name": lines[0].replace("Recipe: ", ""),
            "ingredients": lines[1].replace("Ingredients: ", ""),
            "taste": lines[2].replace("Taste: ", "").lower(),
            "cuisine": lines[3].replace("Cuisine: ", ""),
            "preparation_time": int(lines[4].replace("Preparation Time: ", "").replace(" minutes", "")),
            "instructions": lines[5].replace("Instructions: ", ""),
        })
    return parsed_recipes


def recommend_recipes(preference, available_ingredients, file_path="my_fav_recipes.txt"):
    recipes = parse_recipes(file_path)
    recommended = []

    for recipe in recipes:
        if preference.lower() in recipe["taste"]:
            required_ingredients = {i.split("-")[0].strip() for i in recipe["ingredients"].split(", ")}
            if required_ingredients.issubset(set(available_ingredients)):
                recommended.append(recipe)
    return recommended


def chatbot_response(user_input, available_ingredients):
    # Fetch and filter recipes
    preferences = recommend_recipes(user_input, available_ingredients)

    # Prepare recipe text for the AI model
    recipe_texts = "\n\n".join([f"{r['name']}: {r['ingredients']}" for r in preferences])
    prompt = f"""
    You are a cooking assistant. Based on the user's input "{user_input}" and the available ingredients "{', '.join(available_ingredients)}", suggest recipes.
    Here are the recipes available:
    {recipe_texts}
    Suggest recipes or provide cooking advice.
    """

    # Send the prompt to Gemini AI
    response = gemini_client.chat.create(prompt=prompt)

    return response['message']
