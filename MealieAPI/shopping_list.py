import requests
import json
from MealieAPI.base import * 

base_url = "/api/groups/shopping/lists"

def get_shopping_list(item_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.get("{}{}/{}".format(api_url, base_url, item_id), headers=headers)

    if response.status_code == 200:
        print("\nLista trovata! - Status Code: {}".format(response.status_code))
        return response.json()
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def get_all_shopping_lists(api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    params = {"perPage": 10**4}
    response = requests.get(
        "{}{}".format(api_url, base_url), headers=headers, params=params
    )

    if response.status_code == 200:
        print(
            "\nTrovati {} risultati - Status Code: {}".format(
                response.json()["total"], response.status_code
            )
        )
        return [i for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def search_shopping_list(query, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    params = {"search": query}
    response = requests.get(
        "{}{}".format(api_url, base_url), headers=headers, params=params
    )

    if response.status_code == 200:
        print(
            "\nTrovati {} risultati - Status Code: {}".format(
                response.json()["total"], response.status_code
            )
        )
        return [i for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def delete_shopping_list(slug, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.delete(
        "{}{}/{}".format(api_url, base_url, slug), headers=headers
    )

    if response.status_code == 200:
        print("\nEliminato {} - Status Code: {}".format(slug, response.status_code))
    else:
        print(
            "\nErrore in fase di eliminazione {} - Status Code: {} - Response: {}".format(
                slug, response.status_code, response.text
            )
        )


def create_shopping_list(recipe_name, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    data = {"name": recipe_name}

    response = requests.post(
        "{}{}".format(api_url, base_url),
        data=json.dumps(data, ensure_ascii=False),
        headers=headers,
    )

    if response.status_code == 201:
        print(
            "\nLista creata! - Status Code: {}, Response: {}".format(
                response.status_code, response.json()
            )
        )
        return response.json()
    else:
        print(
            "\nErrore in fase di creazione! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )


def populate_shopping_list(recipe, slug, api_url=mealie_url, token=api_token, delete_if_failed=False):
    headers = get_headers(token)

    response = requests.put(
        "{}{}/{}".format(api_url, base_url, slug),
        data=recipe.serialize(),
        headers=headers,
    )

    if response.status_code == 200:
        print("\nLista popolata! - Status Code: {}".format(response.status_code))
    else:
        print(
            "\nErrore in fase di collegamento! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )
        if delete_if_failed:
            delete_shopping_list(slug, api_url, api_token)


def create_shopping_list_from_url(url, include_tags=False, api_url=mealie_url, token=api_token):
    data = {"url": url, "include_tags": include_tags}
    headers = get_headers(token)

    response = requests.post(
        "{}{}/create-url".format(api_url, base_url),
        data=json.dumps(data),
        headers=headers,
    )

    if response.status_code == 201:
        print(
            "\nLista creata - URL: {}, Include Tags: {}, Status Code: {}, Response: {}".format(
                url, include_tags, response.status_code, response.text
            )
        )
    else:
        print(
            "\nParse Error - URL: {}, Include Tags: {}, Status Code: {}, Response: {}".format(
                url, include_tags, response.status_code, response.text
            )
        )
        return

    slug = response.json()

    if slug[-1].isdigit():
        print(
            "\nAttenzione questa Lista sembrerebbe essere un duplicato! Ti consiglio di andare a controllare"
        )

    return slug


def delete_all_shopping_lists(api_url=mealie_url, token=api_token):
    recipe_list = get_all_shopping_lists(api_url=api_url, token=token)

    for i in recipe_list:
        delete_shopping_list(i.slug)


def empty_list(item_id, api_url=mealie_url, token=api_token):
    shopping_list = get_shopping_list(item_id, api_url=api_url, token=token)

    id_list = [i["id"] for i in shopping_list["listItems"]]

    headers = get_headers(token)
    data = {"ids": id_list}

    response = requests.delete(
        "{}/api/groups/shopping/items".format(api_url), headers=headers, params=data
    )
    if response.status_code == 200:
        print(
            "\nLista svuotata - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )
    else:
        print(
            "\nError - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )
        return
