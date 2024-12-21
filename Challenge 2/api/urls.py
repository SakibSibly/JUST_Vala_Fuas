from django.urls import path
from . import views


urlpatterns = [
    path('ingredients/', views.IngredientList.as_view()),
    path('ingredients/<int:pk>/', views.IngredientDetail.as_view()),
]