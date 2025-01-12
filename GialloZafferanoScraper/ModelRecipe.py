import json

class ModelRecipe:
    imageBase64 = ""
    title = ""
    link = ""
    category = ""
    description = ""
    ingredients = []
    difficulty = ""
    preparationTime = ""
    cookingTime = ""
    servings = ""
    price = ""
    notes = ""
    nutritionals = ""
    calories = ""
    vegetarian = False
    lactoseFree = False
    jsonld = ""

    def toDictionary(self):
        recipe = {
            "imageBase64": self.imageBase64,
            "title": self.title,
            "link": self.link,
            "category": self.category,
            "description": self.description,
            "ingredients": self.ingredients,
            "difficulty": self.difficulty,
            "preparationTime": self.preparationTime,
            "cookingTime": self.cookingTime,
            "servings": self.servings,
            "price": self.price,
            "notes": self.notes,
            "nutritionals": self.nutritionals,
            "calories": self.calories,
            "vegetarian": self.vegetarian,
            "lactoseFree": self.lactoseFree,
            "jsonld": self.jsonld,
        }
        return recipe

def convert_json_to_model_recipe(json_string: str) -> ModelRecipe:
    data = json.loads(json_string)
    recipe = ModelRecipe()
    
    recipe.imageBase64 = data.get("imageBase64", "")
    recipe.title = data.get("title", "")
    recipe.link = data.get("link", "")
    recipe.category = data.get("category", "")
    recipe.description = data.get("description", "")
    recipe.ingredients = data.get("ingredients", [])
    recipe.difficulty = data.get("difficulty", "")
    recipe.preparationTime = data.get("preparationTime", "")
    recipe.cookingTime = data.get("cookingTime", "")
    recipe.servings = data.get("servings", "")
    recipe.price = data.get("price", "")
    recipe.notes = data.get("notes", "")
    recipe.nutritionals = data.get("nutritionals", {})
    recipe.calories = data.get("calories", "")
    recipe.vegetarian = data.get("vegetarian", False)
    recipe.lactoseFree = data.get("lactoseFree", False)
    recipe.jsonld = data.get("jsonld", "")

    return recipe