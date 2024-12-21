from .models import Recipe, Ingredient, RecipeIngredient

def parse_recipe_file(file_path):
    with open(file_path, 'r') as file:
        recipes = file.read().split("\n\n")

    for recipe_text in recipes:
        lines = recipe_text.split("\n")
        name = lines[0].replace("Recipe: ", "")
        ingredients_text = lines[1].replace("Ingredients: ", "")
        taste = lines[2].replace("Taste: ", "").lower()
        cuisine = lines[3].replace("Cuisine: ", "")
        prep_time = int(lines[4].replace("Preparation Time: ", "").replace(" minutes", ""))
        instructions = lines[5].replace("Instructions: ", "")

        recipe = Recipe.objects.create(
            name=name,
            taste=taste,
            cuisine=cuisine,
            preparation_time=prep_time,
            instructions=instructions
        )


        for ing in ingredients_text.split(", "):
            ing_name, ing_details = ing.split("-")
            ing_name = ing_name.strip()
            ing_quantity, ing_unit = ing_details.split(" ")
            ingredient, created = Ingredient.objects.get_or_create(name=ing_name)
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=float(ing_quantity),
                unit=ing_unit
            )
