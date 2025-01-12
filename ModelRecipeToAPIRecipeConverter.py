from GialloZafferanoScraper.ModelRecipe import ModelRecipe
from MealieAPI.models import *
from MealieAPI import unit, food, tag, category
import uuid

# Prendo il ModelRecipe
# Recupero dagli ingredienti del ModelRecipe le unità
# Per ogni unità controllo se esiste già su mealie
# Se non esiste la creo
# In entrambi i casi faccio la GET dell'unità
# Stessa identica operazione per i cibi
# Compilo quindi i RecipeIngredients utilizzando (anche) gli oggetti appena recuperati
# Compilo i RecipeInstructions, Nutritions e Settings
# Per tag e category faccio come per le unità
# Infine creiamo effettivamente l'oggetto di tipo recipe   


def convert_model_recipe_to_recipe(model_recipe: ModelRecipe) -> Recipe:
    # Recupero le Unit
    unit_list = []
    for item in model_recipe.ingredients:
        if "q.b." in item["quantity"]:
            unit_list.append(None)
            continue
        unit_name = item["quantity"].split()[-1] 
        search_res = unit.search_unit(unit_name)
        if len(search_res)>0:
            current_unit = search_res[0]
            unit_list.append(current_unit)
        else:
            current_unit = unit.create_unit(unit_name)
            unit_list.append(current_unit)

            
    # Recupero i Food
    food_list = []
    for item in model_recipe.ingredients:
        food_name = item["name"]
        search_res = food.search_food(food_name)
        if len(search_res)>0:
            current_food = search_res[0]
            food_list.append(current_food)
        else:
            current_food = food.create_food(food_name)
            food_list.append(current_food)


    # Mappiamo gli ingredienti
    recipe_ingredients = [
        RecipeIngredient(
            quantity=float(item["quantity"].split()[-2].replace(",", ".")) if "q.b." not in item["quantity"] else 0.0,  # Assumendo che il formato sia "100 g" o simili
            unit=ingredient_unit,
            food=ingredient_food,
            note=item["quantity"].split("(")[-1].split(")")[0] if len(item["quantity"].split("(")) > 1 else "",
            isFood=True,
            disableAmount="q.b." in item["quantity"],
            display=item["name"] + " " + item["quantity"],
            title=item["name"],
            originalText=item["name"] + " " + item["quantity"],
            referenceId=str(uuid.uuid4())  # Imposta un valore predefinito
        )
        for item, ingredient_unit, ingredient_food in zip(model_recipe.ingredients,unit_list,food_list)
    ]

    # Mappiamo le istruzioni 
    recipe_instructions = [
        RecipeInstruction(
            title=f"Passo {index + 1}",
            text=item,
            ingredientReferences=[] 
        )
        for index, item in enumerate(model_recipe.jsonld["recipeInstructions"])
    ]
    
    # Mappiamo i valori nutrizionali
    nutrition = Nutrition(
        calories=float(model_recipe.calories) if model_recipe.calories else "",
        fatContent=model_recipe.nutritionals.get("Fat", {}).get("value"),
        proteinContent=model_recipe.nutritionals.get("Protein", {}).get("value"),
        carbohydrateContent=model_recipe.nutritionals.get("Carbohydrate", {}).get("value"),
        fiberContent="",
        sodiumContent="",
        sugarContent=""
    ) if model_recipe.nutritionals else None

    # Impostiamo le impostazioni predefinite
    settings = Settings(
        public=True,
        showNutrition=True,
        showAssets=True,
        landscapeView=False,
        disableComments=False,
        disableAmount=False,
        locked=False
    )

            
    # Recupero i Tag
    tag_list = []
    for tag_name in model_recipe.jsonld["keywords"].split(", "):
        search_res = tag.search_tag(tag_name)
        if len(search_res)>0:
            current_tag = search_res[0]
            tag_list.append(current_tag)
        else:
            current_tag = tag.create_tag(tag_name)
            tag_list.append(current_tag)

        
    if not model_recipe.category:
        model_recipe.category = model_recipe.jsonld["recipeCategory"]
    # Recupero i Category
    category_list = []
    for category_name in [model_recipe.category]:
        if not model_recipe.category:
            category_list.append(None)
        search_res = category.search_category(category_name)
        if len(search_res)>0:
            current_category = search_res[0]
            category_list.append(current_category)
        else:
            current_category = category.create_category(category_name)
            category_list.append(current_category)


    # Creiamo l'oggetto Recipe con i valori aggiuntivi dal dizionario
    return Recipe(
        id=str(uuid.uuid4()),
        userId=str(uuid.uuid4()),
        groupId=str(uuid.uuid4()),
        name=model_recipe.title,
        slug=model_recipe.title.lower().replace(" ", "-"),
        image=model_recipe.imageBase64,
        recipeYield=model_recipe.servings,
        totalTime=model_recipe.preparationTime,
        prepTime=model_recipe.preparationTime,
        cookTime=model_recipe.cookingTime,
        performTime="",
        description=model_recipe.description,
        recipeCategory=category_list,
        tags=tag_list,
        tools=[],  # Popolare se i tools sono disponibili
        rating=int(model_recipe.jsonld["aggregateRating"]["ratingValue"]),
        orgURL=model_recipe.link,
        dateAdded="2025-01-10",
        dateUpdated="2025-01-10",
        createdAt="2025-01-10",
        updateAt="2025-01-10",
        lastMade="2025-01-10",
        recipeIngredient=recipe_ingredients,
        recipeInstructions=recipe_instructions,
        nutrition=nutrition,
        settings=settings,
        assets=[],
        notes=[],
        extras={},
        comments=[]
    )
