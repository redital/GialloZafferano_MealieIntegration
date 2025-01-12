from MealieAPI.models import *

def deserialize_ingredient_unit(data: dict) -> IngredientUnit:
    return IngredientUnit(
        name=data.get("name", None),
        id=data.get("id", None),
        description=data.get("description", ""),
        extras=data.get("extras", {}),
        fraction=data.get("fraction", False),
        abbreviation=data.get("abbreviation", ""),
        useAbbreviation=data.get("useAbbreviation", False),
    )

def deserialize_ingredient_food(data: dict) -> IngredientFood:
    return IngredientFood(
        name=data.get("name", None),
        id=data.get("id", None),
        description=data.get("description", ""),
        puralName=data.get("puralName", ""),
        extras=data.get("extras", {}),
        onHand=data.get("onHand", False),
        aliases=data.get("aliases", []),
    )

def deserialize_recipe_ingredient(data: dict) -> RecipeIngredient:
    return RecipeIngredient(
        food=deserialize_ingredient_food(data.get("food", {})) if data.get("food") else None,
        quantity=data.get("quantity", 0.0),
        isFood=data.get("isFood", False),
        disableAmount=data.get("disableAmount", False),
        display=data.get("display", ""),
        unit=deserialize_ingredient_unit(data.get("unit", {})) if data.get("unit") else None,
        note=data.get("note", None),
        title=data.get("title", None),
        originalText=data.get("originalText", None),
        referenceId=data.get("referenceId", None),
    )

def deserialize_recipe_instruction(data: dict) -> RecipeInstruction:
    return RecipeInstruction(
        title=data.get("title", ""),
        text=data.get("text", ""),
        ingredientReferences=data.get("ingredientReferences", []),
        id=data.get("id", None),
    )

def deserialize_nutrition(data: dict) -> Nutrition:
    return Nutrition(
        calories=data.get("calories", None),
        fatContent=data.get("fatContent", None),
        proteinContent=data.get("proteinContent", None),
        carbohydrateContent=data.get("carbohydrateContent", None),
        fiberContent=data.get("fiberContent", None),
        sodiumContent=data.get("sodiumContent", None),
        sugarContent=data.get("sugarContent", None),
    )

def deserialize_settings(data: dict) -> Settings:
    return Settings(
        public=data.get("public", False),
        showNutrition=data.get("showNutrition", False),
        showAssets=data.get("showAssets", False),
        landscapeView=data.get("landscapeView", False),
        disableComments=data.get("disableComments", False),
        disableAmount=data.get("disableAmount", False),
        locked=data.get("locked", False),
    )

def deserialize_recipe_tag(data: dict) -> RecipeTag:
    return RecipeTag(
        name=data.get("name", None),
        slug=data.get("slug", None),
        id=data.get("id", None),
    )

def deserialize_recipe_category(data: dict) -> RecipeCategory:
    return RecipeCategory(
        name=data.get("name", None),
        slug=data.get("slug", None),
        id=data.get("id", None),
    )

def deserialize_recipe_tool(data: dict) -> RecipeTag:
    return RecipeTool(
        name=data.get("name", None),
        slug=data.get("slug", None),
        id=data.get("id", None),
        onHand=data.get("onHand", False),
    )

def deserialize_recipe(data: dict) -> Recipe:
    return Recipe(
        id=data.get("id", None),
        userId=data.get("userId", None),
        groupId=data.get("groupId", None),
        name=data.get("name", None),
        slug=data.get("slug", None),
        image=data.get("image", None),
        recipeYield=data.get("recipeYield", None),
        totalTime=data.get("totalTime", None),
        prepTime=data.get("prepTime", None),
        cookTime=data.get("cookTime", None),
        performTime=data.get("performTime", None),
        description=data.get("description", None),
        recipeCategory=[deserialize_recipe_category(instruction) for instruction in data.get("recipeCategory", [])],
        tags=[deserialize_recipe_tag(instruction) for instruction in data.get("tags", [])],
        tools=[deserialize_recipe_tool(instruction) for instruction in data.get("tools", [])],
        rating=data.get("rating", None),
        orgURL=data.get("orgURL", None),
        dateAdded=data.get("dateAdded", None),
        dateUpdated=data.get("dateUpdated", None),
        createdAt=data.get("createdAt", None),
        updateAt=data.get("updateAt", None),
        lastMade=data.get("lastMade", None),
        recipeIngredient=[
            deserialize_recipe_ingredient(ingredient) for ingredient in data.get("recipeIngredient", [])
        ],
        recipeInstructions=[
            deserialize_recipe_instruction(instruction) for instruction in data.get("recipeInstructions", [])
        ],
        nutrition=deserialize_nutrition(data.get("nutrition", {})),
        settings=deserialize_settings(data.get("settings", {})),
        assets=data.get("assets", []),
        notes=data.get("notes", []),
        extras=data.get("extras", {}),
        comments=data.get("comments", []),
    )
