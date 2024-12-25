from main import * 
from ModelRecipeToAPIRecipeConverter import modelRecipeToAPIRecipe



def downloadFirstRecipeFromGialloZafferano():
    totalPages = countTotalPages() + 1
    # for pageNumber in range(1,totalPages):
    for pageNumber in tqdm(range(1, totalPages), desc="pages…", ascii=False, ncols=75):
        linkList = "https://www.giallozafferano.it/ricette-cat/page" + str(pageNumber)
        response = requests.get(linkList)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(attrs={"class": "gz-title"}):
            link = tag.a.get("href")
            recipe = saveRecipe(link)
            
            with open("RecipesFormatted/{}.json".format(recipe.title), "w") as file:
                file.write(json.dumps(dict(modelRecipeToAPIRecipe(recipe)), ensure_ascii=False))
            break
        break

def getAllRecipesListFromGialloZafferano():
    totalPages = countTotalPages() + 1
    # for pageNumber in range(1,totalPages):
    result = []
    for pageNumber in tqdm(range(1, totalPages), desc="pages…", ascii=False, ncols=75):
        linkList = "https://www.giallozafferano.it/ricette-cat/page" + str(pageNumber)
        response = requests.get(linkList)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(attrs={"class": "gz-title"}):
            link = tag.a.get("href")
            result.append(link)

    
    with open("lista_link.json", "w") as file:
        file.write(json.dumps(result, ensure_ascii=False))

    return result

downloadFirstRecipeFromGialloZafferano()