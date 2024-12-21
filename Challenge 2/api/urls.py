from django.urls import path
from . import views


urlpatterns = [
    path('ingredients/', views.IngredientList.as_view()),
    path('ingredients/<int:pk>/', views.IngredientDetail.as_view()),
    path('parse-recipe/', views.ParseRecipe.as_view(), name='parse_recipe'),
    path('favourite-recipe/', views.FavouriteRecipeTextView.as_view(), name='recipe_text_upload'),
    path('recipe-image/', views.RecipeImageUpload.as_view(), name='recipe_image_upload'),
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),

]