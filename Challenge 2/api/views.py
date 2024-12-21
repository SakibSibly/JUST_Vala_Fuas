from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Ingredient, Recipe, RecipeIngredient
from .serializers import IngredientSerializer, RecipeSerializer, ChatbotInputSerializer
import pytesseract
from PIL import Image



class IngredientList(APIView):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class IngredientDetail(APIView):
    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def put(self, request, pk):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ingredient = self.get_object(pk)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ParseRecipe(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        self.parse_recipe_file(file)
        return Response({"message": "Recipe saved successfully."}, status=status.HTTP._201_CREATED)
    
        
    def parse_recipe_file(self, file_path):
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


class FavouriteRecipeTextView(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Recipe saved successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeImageUpload(APIView):
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        image = request.FILES['image']
        pil_image = Image.open(image)
        extracted_text = pytesseract.image_to_string(pil_image)

        return Response({"message": "Image processed and recipe saved."}, status=status.HTTP_201_CREATED)


class ChatbotView(APIView):
    from dotenv import load_dotenv
    import os
    from gemini import GeminiClient  

    
    load_dotenv()

    
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    gemini_client = GeminiClient(api_key=GEMINI_API_KEY)

    def parse_recipes(self, file_path):
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


    def recommend_recipes(self, preference, available_ingredients, file_path="my_fav_recipes.txt"):
        recipes = self.parse_recipes(file_path)
        recommended = []

        for recipe in recipes:
            if preference.lower() in recipe["taste"]:
                required_ingredients = {i.split("-")[0].strip() for i in recipe["ingredients"].split(", ")}
                if required_ingredients.issubset(set(available_ingredients)):
                    recommended.append(recipe)
        return recommended


    def chatbot_response(self, user_input, available_ingredients):
        
        preferences = self.recommend_recipes(user_input, available_ingredients)

        
        recipe_texts = "\n\n".join([f"{r['name']}: {r['ingredients']}" for r in preferences])
        prompt = f"""
        You are a cooking assistant. Based on the user's input "{user_input}" and the available ingredients "{', '.join(available_ingredients)}", suggest recipes.
        Here are the recipes available:
        {recipe_texts}
        Suggest recipes or provide cooking advice.
        """

        
        response = self.gemini_client.chat.create(prompt=prompt)

        return response['message']

    def post(self, request):
        serializer = ChatbotInputSerializer(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data['message']
            
            available_ingredients = [ingredient.name for ingredient in Ingredient.objects.all()]
            
            
            response = self.chatbot_response(user_message, available_ingredients)
            return Response({"reply": response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)