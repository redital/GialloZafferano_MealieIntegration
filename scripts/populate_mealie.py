from ..GialloZafferanoScraper.main import * 
from ..creazione_ibrida_ricette import creazione_ibrida_ricette
from ..MealieAPI import recipe

def populate_mealie():
    mealie_recipes = recipe.get_all_recipes()
    used_links = [i.orgURL for i in mealie_recipes]
    totalPages = countTotalPages() + 1
    for pageNumber in tqdm(range(1, totalPages), desc="pages…", ascii=False, ncols=75):
        linkList = "https://www.giallozafferano.it/ricette-cat/page" + str(pageNumber)
        response = requests.get(linkList)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(attrs={"class": "gz-title"}):
            link = tag.a.get("href")
            if link in used_links:
                print("link {} già usato".format(link))
            else:
                try:
                    creazione_ibrida_ricette(link)
                except:
                    handle_failure(link)
                    exit()


def handle_failure(url):
    print("c'è stato un errore")
    mealie_recipes = recipe.get_all_recipes()
    failed_recipe = [i for i in mealie_recipes if i.orgURL == url]
    if len(failed_recipe)==0:
        print("Il fallimento è accaduto prima della creazione della ricetta\nLink: {}".format(url))
        return
    
    failed_recipe = failed_recipe[0]
    recipe.delete_recipe(failed_recipe.slug)
    print("Ricetta il cui caricamento è fallito: {} \nLink: {}".format(failed_recipe.name, url))
    return
    
populate_mealie()