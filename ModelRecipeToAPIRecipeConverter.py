from GialloZafferanoScraper.ModelRecipe import ModelRecipe
from MealieAPI.models import *
from MealieAPI import unit, food, tag, category
import uuid
from thefuzz import fuzz

soglia_fuzzy_matching = 75

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

def compute_unit_list(ingredients):
    unit_list = []
    for item in ingredients:
        if quantity_parser(item["quantity"])["unit"] == None:
            unit_list.append(None)
        if len(item["quantity"].split()) == 1:
            unit_list.append(None)
            continue
        unit_name = item["quantity"].split()[-1] 
        search_res = unit.search_unit(unit_name)
        if len(search_res)>0:
            score_dict = [{"item":i, "score":fuzz.ratio(unit_name, i.name)} for i in search_res]
            print(score_dict)
            best_res = [i["item"] for i in score_dict if i["score"] == max([i["score"] for i in score_dict])][0]
            if max([i["score"] for i in score_dict]) > soglia_fuzzy_matching:
                current_unit = best_res
                unit_list.append(current_unit)
            else:
                current_unit = unit.create_unit(unit_name)
                unit_list.append(current_unit)
        else:
            current_unit = unit.create_unit(unit_name)
            unit_list.append(current_unit)
    return unit_list

def compute_food_list(ingredients):
    food_list = []
    for item in ingredients:
        food_name = item["name"]
        search_res = food.search_food(food_name)
        if len(search_res)>0:
            score_dict = [{"item":i, "score":fuzz.ratio(food_name, i.name)} for i in search_res]
            print(score_dict)
            best_res = [i["item"] for i in score_dict if i["score"] == max([i["score"] for i in score_dict])][0]
            if max([i["score"] for i in score_dict]) > soglia_fuzzy_matching:
                current_food = best_res
                food_list.append(current_food)
            else:
                current_food = food.create_food(food_name)
                food_list.append(current_food)
        else:
            current_food = food.create_food(food_name)
            food_list.append(current_food)
    return food_list

def compute_tag_list(keywords):
    tag_list = []
    for tag_name in keywords:
        search_res = tag.search_tag(tag_name)
        if len(search_res)>0:
            score_dict = [{"item":i, "score":fuzz.ratio(tag_name, i.name)} for i in search_res]
            print(score_dict)
            best_res = [i["item"] for i in score_dict if i["score"] == max([i["score"] for i in score_dict])][0]
            if max([i["score"] for i in score_dict]) > soglia_fuzzy_matching:
                current_unit = best_res
                tag_list.append(current_unit)
            else:
                current_unit = tag.create_tag(tag_name)
                tag_list.append(current_unit)
            current_tag = search_res[0]
            tag_list.append(current_tag)
        else:
            current_tag = tag.create_tag(tag_name)
            tag_list.append(current_tag)
    return tag_list

def compute_category_list(category_text):
    category_list = []
    for category_name in [category_text]:
        if not category_text:
            category_list.append(None)
        search_res = category.search_category(category_name)
        if len(search_res)>0:
            score_dict = [{"item":i, "score":fuzz.ratio(category_name, i.name)} for i in search_res]
            print(score_dict)
            best_res = [i["item"] for i in score_dict if i["score"] == max([i["score"] for i in score_dict])][0]
            if max([i["score"] for i in score_dict]) > soglia_fuzzy_matching:
                current_unit = best_res
                category_list.append(current_unit)
            else:
                current_unit = category.create_category(category_name)
                category_list.append(current_unit)
            current_category = search_res[0]
            category_list.append(current_category)
        else:
            current_category = category.create_category(category_name)
            category_list.append(current_category)
    return category_list


def convert_model_recipe_to_recipe(model_recipe: ModelRecipe) -> Recipe:
    # Recupero le Unit
    unit_list = compute_unit_list(model_recipe.ingredients)

    # Recupero i Food
    food_list = compute_food_list(model_recipe.ingredients)


    # Mappiamo gli ingredienti
    recipe_ingredients = [
        RecipeIngredient(
            quantity=quantity_parser(item["quantity"])["number"],  # Assumendo che il formato sia "100 g" o simili
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
    tag_list = compute_tag_list(model_recipe.jsonld["keywords"].split(", "))

        
    # Recupero i Category
    if not model_recipe.category:
        model_recipe.category = model_recipe.jsonld["recipeCategory"]
    category_list = compute_category_list(model_recipe.category)


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

import unicodedata

def quantity_parser(text):
    if "q.b." in text:
        return {"number":None,"unit":None}
    numeric_indexes = [i for i,t in enumerate(text.split()) if t.isnumeric()]
    if len(numeric_indexes) == 0:
        return {"number":None,"unit":text}
    text = " ".join(text.split()[numeric_indexes[0]:])
    number = None
    if len(text.split()) == 1:
        try: 
            number = float(text.replace(",", "."))
        except: number = unicodedata.numeric(text.replace(",", "."))
        return {"number":number,"unit":None}
    try: number = float(text.split()[0].replace(",", "."))
    except: number = unicodedata.numeric(text.split()[0].replace(",", "."))
    return {"number":number,"unit":" ".join(text.split()[1:])}