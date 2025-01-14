import requests
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


def delete_shopping_list(item_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.delete(
        "{}{}/{}".format(api_url, base_url, item_id), headers=headers
    )

    if response.status_code == 200:
        print("\nEliminato {} - Status Code: {}".format(item_id, response.status_code))
    else:
        print(
            "\nErrore in fase di eliminazione {} - Status Code: {} - Response: {}".format(
                item_id, response.status_code, response.text
            )
        )


def delete_all_shopping_lists(api_url=mealie_url, token=api_token):
    recipe_list = get_all_shopping_lists(api_url=api_url, token=token)

    for i in recipe_list:
        delete_shopping_list(i["id"])


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
