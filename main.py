from fileinput import filename
import requests

# import urllib.request
from bs4 import BeautifulSoup
import re

# import string
from string import digits
import json
from ModelRecipe import ModelRecipe
import os
import base64
from tqdm import tqdm


debug = False
folderRecipes = "recipes"

fileName = "URLS"
filePath = folderRecipes + "/" + fileName


def loadUrlsFile():
    fileObj = open(filePath, "r")  # opens the file in read mode
    currentUrls = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return currentUrls


def saveRecipe(linkRecipeToDownload) -> ModelRecipe:
    soup = downloadPage(linkRecipeToDownload)
    title = findTitle(soup)

    filePath = calculateFilePath(title)
    if os.path.exists(filePath):
        return

    ingredients = findIngredients(soup)
    description = findDescription(soup)
    category = findCategory(soup)
    imageBase64 = findImage(soup)
    props = findProps(soup)
    nutritionals = findNutritionalInfo(soup)
    calories = findCalories(soup)
    other = findOther(soup)
    jsonld = get_json_ld(soup)

    modelRecipe = ModelRecipe()
    modelRecipe.title = title
    modelRecipe.link = linkRecipeToDownload
    modelRecipe.ingredients = ingredients
    modelRecipe.description = description
    modelRecipe.category = category
    modelRecipe.imageBase64 = imageBase64
    modelRecipe.difficulty = props["difficulty"]
    modelRecipe.preparationTime = props["preparationTime"]
    modelRecipe.cookingTime = props["cookingTime"]
    modelRecipe.servings = props["servings"]
    modelRecipe.price = props["cost"]
    modelRecipe.notes = props["notes"]
    modelRecipe.nutritionals = nutritionals
    modelRecipe.calories = calories
    modelRecipe.vegetarian = other["vegetarian"]
    modelRecipe.lactoseFree = other["lactoseFree"]
    modelRecipe.jsonld = jsonld

    #createFileJson(modelRecipe.toDictionary(), filePath)

    return modelRecipe


def findTitle(soup):
    tag = soup.find(attrs={"class": "gz-title-recipe gz-mBottom2x"})
    return tag.text


def findCalories(soup):
    tag = soup.find(attrs={"class": "gz-text-calories-total"})
    if tag is not None:
        return tag.text.strip()


def findProps(soup):
    properties = {
        "difficulty": "",
        "preparationTime": "",
        "cookingTime": "",
        "servings": "",
        "cost": "",
        "notes": "",
    }
    for tag in soup.find_all(attrs={"class": "gz-name-featured-data"}):
        propName = tag.contents[0]
        propValue = tag.strong.string

        if propName.text == "Nota":
            propName = "Note"
            propValue = tag.contents[1]

        if propName.startswith("Difficolt"):
            properties["difficulty"] = propValue
        elif propName.startswith("Preparazione"):
            properties["preparationTime"] = propValue
        elif propName.startswith("Cottura"):
            properties["cookingTime"] = propValue
        elif propName.startswith("Dosi per"):
            properties["servings"] = propValue
        elif propName.startswith("Costo"):
            properties["cost"] = propValue
        elif propName.startswith("Note"):
            properties["notes"] = propValue
    return properties


def findOther(soup):
    other = {
        "vegetarian": False,
        "lactoseFree": False,
    }

    for tag in soup.find_all(attrs={"class": "gz-name-featured-data-other"}):
        if tag.string == "Vegetariano":
            other["vegetarian"] = True
        elif tag.string == "Senza lattosio":
            other["lactoseFree"] = True

    return other


def findNutritionalInfo(soup):
    nutritionalInfo = {}
    nutritionalsTag = soup.find(attrs={"class": "gz-list-macros"})
    if nutritionalsTag is not None:
        for item in nutritionalsTag.find_all("li"):
            name = item.find("span", attrs={"class": "gz-list-macros-name"}).string
            unit = item.find("span", attrs={"class": "gz-list-macros-unit"}).string
            value = item.find("span", attrs={"class": "gz-list-macros-value"}).string
            nutritionalInfo[name] = {"unit": unit, "value": value}
        return nutritionalInfo


def findIngredients(soup):
    allIngredients = []
    for tag in soup.find_all(attrs={"class": "gz-ingredient"}):
        nameIngredient = tag.a.string
        contents = tag.span.contents[0]
        quantityProduct = re.sub(r"\s+", " ", contents).strip()
        ingredient = {
            "name": nameIngredient,
            "quantity": quantityProduct,
        }
        allIngredients.append(ingredient)
    return allIngredients


def findDescription(soup):
    allDescription = ""
    for tag in soup.find_all(attrs={"class": "gz-content-recipe-step"}):
        removeNumbers = str.maketrans("", "", digits)
        if hasattr(tag.p, "text"):
            description = tag.p.text.translate(removeNumbers)
            allDescription = allDescription + description.replace("\xa0", " ")
    return allDescription


def findCategory(soup):
    for tag in soup.find_all(attrs={"class": "gz-breadcrumb"}):
        category = tag.li.a.string
        return category


def get_json_ld(soup):
    return json.loads(
        "".join(soup.find("script", {"type": "application/ld+json"}).contents)
    )


def findImage(soup):
    # Find the first picture tag
    pictures = soup.find("picture", attrs={"class": "gz-featured-image"})

    # Fallback: find a div with class `gz-featured-image-video gz-type-photo`
    if pictures is None:
        pictures = soup.find(
            "div", attrs={"class": "gz-featured-image-video gz-type-photo"}
        )

    imageSource = pictures.find("img")

    # Most of the times the url is in the `data-src` attribute
    imageURL = imageSource.get("data-src")

    # Fallback: if not found in `data-src` look for the `src` attr
    # Most likely, recipes which have the `src` attr
    # instead of the `data-src` one
    # are the older ones.
    # As a matter of fact, those are the ones enclosed
    # in <div> tags instead of <picture> tags (supported only on html5 and onward)
    if imageURL is None:
        imageURL = imageSource.get("src")

    imageToBase64 = str(base64.b64encode(requests.get(imageURL).content))
    imageToBase64 = imageToBase64[2 : len(imageToBase64) - 1]
    return imageToBase64


def calculateFilePath(title):
    compact_name = title.replace(" ", "_").lower()
    return folderRecipes + "/" + compact_name + ".json"


def createFileJson(data, path):
    with open(path, "w") as file:
        file.write(json.dumps(data, ensure_ascii=False))


def updateDownloadedLinks(link, path):
    with open(path, "a") as file:
        file.write(link, ensure_ascii=False)


def downloadPage(linkToDownload):
    response = requests.get(linkToDownload)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def appendNewUrlsAndEmpty(newUrls):
    fileUrl = open(filePath, "a")
    for line in newUrls:
        fileUrl.write(line + "\r")
    fileUrl.close()
    return []


def downloadAllRecipesFromGialloZafferano(currentUrls):
    totalPages = countTotalPages() + 1
    # for pageNumber in range(1,totalPages):
    newUrls = []
    for pageNumber in tqdm(range(1, totalPages), desc="pages…", ascii=False, ncols=75):
        linkList = "https://www.giallozafferano.it/ricette-cat/page" + str(pageNumber)
        response = requests.get(linkList)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(attrs={"class": "gz-title"}):
            link = tag.a.get("href")
            if link in currentUrls:
                break
            saveRecipe(link)
            newUrls.append(link)

        if len(newUrls) > 100:
            newUrls = appendNewUrlsAndEmpty(newUrls)

    appendNewUrlsAndEmpty(newUrls)


def countTotalPages():
    numberOfPages = 0
    linkList = "https://www.giallozafferano.it/ricette-cat"
    response = requests.get(linkList)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup.find_all(attrs={"class": "disabled total-pages"}):
        numberOfPages = int(tag.text)
    return numberOfPages


if __name__ == "__main__":
    if not os.path.exists(folderRecipes):
        os.makedirs(folderRecipes)
    if not os.path.exists(filePath):
        with open(filePath, "w") as file:
            pass
    currentUrls = loadUrlsFile()
    downloadAllRecipesFromGialloZafferano(currentUrls)
