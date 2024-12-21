Challenge 2
---

### **1. Route: `/api/ingredients`**
**Method**: GET  
**Description**: Retrieves all available ingredients.  
**Sample Response**:  
```json
[
  {
    "id": 1,
    "name": "sugar",
    "quantity": "500g"
  },
  {
    "id": 2,
    "name": "flour",
    "quantity": "1kg"
  }
]
```

---

### **2. Route: `/api/ingredients`**
**Method**: POST  
**Description**: Adds a new ingredient to the database.  
**Sample Payload**:  
```json
{
  "name": "butter",
  "quantity": "200g"
}
```
**Sample Response**:  
```json
{
  "id": 3,
  "name": "butter",
  "quantity": "200g"
}
```

---

### **3. Route: `/api/ingredients/<int:id>`**
**Method**: PATCH  
**Description**: Updates an existing ingredient's quantity.  
**Sample Payload**:  
```json
{
  "quantity": "250g"
}
```
**Sample Response**:  
```json
{
  "id": 3,
  "name": "butter",
  "quantity": "250g"
}
```

---

### **4. Route: `/api/favourite-recipe`**
**Method**: GET  
**Description**: Retrieves all stored recipes.  
**Sample Response**:  
```json
[
  {
    "id": 1,
    "name": "Chocolate Pancakes",
    "ingredients": [
      "flour",
      "sugar",
      "cocoa powder"
    ],
    "taste": "sweet",
    "cuisine": "dessert",
    "preparation_time": 20,
    "instructions": "Mix ingredients and cook on a pan."
  },
  {
    "id": 2,
    "name": "Tomato Soup",
    "ingredients": [
      "tomatoes",
      "onion",
      "garlic"
    ],
    "taste": "savory",
    "cuisine": "appetizer",
    "preparation_time": 15,
    "instructions": "Blend tomatoes and simmer with spices."
  }
]
```

---

### **5. Route: `/api/favourite-recipe`**
**Method**: POST  
**Description**: Adds a new recipe to the database.  
**Sample Payload**:  
```json
{
  "name": "Vanilla Ice Cream",
  "ingredients": ["milk", "sugar", "vanilla extract"],
  "taste": "sweet",
  "cuisine": "dessert",
  "preparation_time": 60,
  "instructions": "Mix ingredients and freeze."
}
```
**Sample Response**:  
```json
{
  "id": 3,
  "name": "Vanilla Ice Cream",
  "ingredients": ["milk", "sugar", "vanilla extract"],
  "taste": "sweet",
  "cuisine": "dessert",
  "preparation_time": 60,
  "instructions": "Mix ingredients and freeze."
}
```

---

### **6. Route: `/api/chatbot`**
**Method**: POST  
**Description**: Interacts with the chatbot to get recipe suggestions based on user preferences and available ingredients.  
**Sample Payload**:  
```json
{
  "message": "I want something sweet today"
}
```
**Sample Response**:  
```json
{
  "reply": "Based on your preferences, I recommend trying Chocolate Pancakes or Vanilla Ice Cream."
}
```

---

### **7. Route: `/api/recipe-image`**
**Method**: POST  
**Description**: Uploads a new recipe from an image or text.  
**Sample Payload**:  
```json
{
  "text": "Recipe: Lemon Cake\nIngredients: flour - 200g, sugar - 100g, lemon juice - 50ml\nTaste: sweet\nCuisine: dessert\nPreparation Time: 45 minutes\nInstructions: Mix all ingredients and bake for 30 minutes."
}
```
**Sample Response**:  
```json
{
  "id": 4,
  "name": "Lemon Cake",
  "ingredients": ["flour", "sugar", "lemon juice"],
  "taste": "sweet",
  "cuisine": "dessert",
  "preparation_time": 45,
  "instructions": "Mix all ingredients and bake for 30 minutes."
}
```

---

### **8. Route: `/api/recipe-image/<int:id>`**
**Method**: DELETE  
**Description**: Deletes a recipe from the database.  
**Sample Response**:  
```json
{
  "message": "Recipe deleted successfully"
}
```

### **9. Route: `/parse-recipe/`**
**Method**: POST  
**Description**: Accepts recipe data (as text) to parse and store details like ingredients, cuisine, taste, preparation time, and instructions into the database.  
**Sample Payload**:  
```json
{
    "recipe_text": "Recipe: Spaghetti Bolognese\nIngredients: spaghetti - 200g, minced beef - 300g, tomato sauce - 200ml\nTaste: savory\nCuisine: Italian\nPreparation Time: 40 minutes\nInstructions: Boil spaghetti. Cook minced beef with tomato sauce and serve together."
}
```
**Sample Response**:  
**Success Response**:  
```json
{
    "id": 1,
    "name": "Spaghetti Bolognese",
    "ingredients": [
        "spaghetti",
        "minced beef",
        "tomato sauce"
    ],
    "taste": "savory",
    "cuisine": "Italian",
    "preparation_time": 40,
    "instructions": "Boil spaghetti. Cook minced beef with tomato sauce and serve together."
}
```
**Error Response**:  
```json
{
    "error": "Failed to parse recipe text. Please check the format."
}
```

---
