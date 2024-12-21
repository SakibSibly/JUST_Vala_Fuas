from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        write_only=True
    )

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'taste', 'cuisine', 'preparation_time', 'instructions', 'ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ing in ingredients_data:
            ingredient, _ = Ingredient.objects.get_or_create(name=ing['name'])
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=ing['quantity'],
                unit=ing['unit']
            )
        return recipe
