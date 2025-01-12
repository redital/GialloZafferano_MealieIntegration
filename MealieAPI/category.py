import requests
import json
from MealieAPI.base import * 
from MealieAPI.deserialize_models import deserialize_recipe_category

base_url = "/api/organizers/categories"

def get_category(category_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.get("{}{}/{}".format(api_url, base_url, category_id), headers=headers)

    if response.status_code == 200:
        print("\Strumento trovato! - Status Code: {}".format(response.status_code))
        return deserialize_recipe_category(response.json())
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def get_all_categories(api_url=mealie_url, token=api_token):
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
        return [deserialize_recipe_category(i) for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def search_category(query, api_url=mealie_url, token=api_token):
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
        return [deserialize_recipe_category(i) for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def delete_category(category_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.delete(
        "{}{}/{}".format(api_url, base_url, category_id), headers=headers
    )

    if response.status_code == 200:
        print("\nEliminato {} - Status Code: {}".format(category_id, response.status_code))
    else:
        print(
            "\nErrore in fase di eliminazione {} - Status Code: {} - Response: {}".format(
                category_id, response.status_code, response.text
            )
        )


def create_category(category_name, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    data = {"name": category_name}

    response = requests.post(
        "{}{}".format(api_url, base_url),
        data=json.dumps(data, ensure_ascii=False),
        headers=headers,
    )

    if response.status_code == 201:
        print(
            "\nCategory creato! - Status Code: {}, Response: {}".format(
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


def populate_category(category, category_id, api_url=mealie_url, token=api_token, delete_if_failed=False):
    headers = get_headers(token)

    response = requests.put(
        "{}{}/{}".format(api_url, base_url, category_id),
        data=category.serialize(),
        headers=headers,
    )

    if response.status_code == 200:
        print("\ncategory popolato! - Status Code: {}".format(response.status_code))
    else:
        print(
            "\nErrore in fase di collegamento! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )
        if delete_if_failed:
            delete_category(category_id, api_url, api_token)

