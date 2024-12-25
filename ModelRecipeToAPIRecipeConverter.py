from ModelRecipe import ModelRecipe
from mealieapi.recipes import Recipe

def modelRecipeToAPIRecipe (modelRecipe: ModelRecipe) -> Recipe:
    print(una_qualche_funzione_di_parsing(modelRecipe.description))
    print(una_qualche_funzione_di_parsing(modelRecipe.notes))
    recipe = Recipe(
        _client = None,
        name=modelRecipe.jsonld["name"],
        description=modelRecipe.jsonld["description"],
        image=modelRecipe.imageBase64,
        recipe_yield=modelRecipe.jsonld["recipeYield"],
        recipe_ingredient=modelRecipe.jsonld["recipeIngredient"], # Avrei anche le quantità separate dai nomi ma lui vuole una lista di stringhe
        recipe_instructions=una_qualche_funzione_di_parsing(modelRecipe.description),
        tags=list(modelRecipe.jsonld["keywords"].split(", ")),
        notes=una_qualche_funzione_di_parsing(modelRecipe.notes),
        rating=int(modelRecipe.jsonld["aggregateRating"]["ratingValue"]),
        id=None,
        settings=None, # Non ho idea di cosa siano
        total_time=modelRecipe.jsonld["totalTime"],
        prep_time=modelRecipe.jsonld["prepTime"],
        perform_time=modelRecipe.jsonld["cookTime"],
        nutrition=None, # Ho l'informazione ma potrebbe essere complessa e adesso mi rompo
        date_added=None,
        date_updated=None, # Non so ancora come voglio gestire le date ma le ho
        org_url=modelRecipe.link,

    )

    return recipe

def una_qualche_funzione_di_parsing(text:str) -> list[dict[str, str]]:
    return [{"passaggio_unico": text}]

