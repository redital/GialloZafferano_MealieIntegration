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
