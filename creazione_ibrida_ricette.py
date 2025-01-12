# Recupero il link alla ricetta da Giallo Zafferano 
# Scarico le informazioni con lo scraper su e salvo sul ModelRecipe 
# Converto il ModelRecipe in Recipe 
# Creo tramite url la ricetta su Mealie 
# OPZIONE 1
# Faccio una GET della ricetta 
# Scelgo le feature che voglio prendere dall'oggetto ottenuto da scraper 
# Copio le feature interessate sull'oggetto ottenuto dalla get
# Faccio una PUT della ricetta 
# OPZIONE 2 
# Faccio una PATCH dee feature interessate

from ModelRecipeToAPIRecipeConverter import convert_model_recipe_to_recipe
from main import saveRecipe
from MealieAPI import recipe 

def creazione_ibrida_ricette(url, ingredients = True, category = True, tags = True, ):
    
    recipe_model_instance = saveRecipe(url)

    recipe_from_scraping = convert_model_recipe_to_recipe(recipe_model_instance)

    created_recipe_slug = recipe.create_recipe_from_url(url)

    created_recipe = recipe.get_recipe(created_recipe_slug)

    if ingredients:
        created_recipe.recipeIngredient = recipe_from_scraping.recipeIngredient

        created_recipe.settings.disableAmount = False

    if category:
        created_recipe.recipeCategory = recipe_from_scraping.recipeCategory

    #if tags:
    #    created_recipe.tags = recipe_from_scraping.tags

    recipe.populate_recipe(created_recipe,created_recipe_slug,delete_if_failed=True)


