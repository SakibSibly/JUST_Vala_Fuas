from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', related_name='recipes'
    )
    taste = models.CharField(max_length=50, choices=[
        ('sweet', 'Sweet'),
        ('savory', 'Savory'),
        ('spicy', 'Spicy'),
        ('bitter', 'Bitter'),
        ('sour', 'Sour'),
    ])
    cuisine = models.CharField(max_length=100)
    preparation_time = models.PositiveIntegerField()
    reviews = models.FloatField(default=0.0)
    instructions = models.TextField()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)  

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.recipe.name}"


class ShoppingList(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='shopping_list')
    quantity = models.FloatField()  
    unit = models.CharField(max_length=50)  

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} to buy"
