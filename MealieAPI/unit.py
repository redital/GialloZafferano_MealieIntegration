import requests
import json
from MealieAPI.base import * 
from MealieAPI.deserialize_models import deserialize_ingredient_unit

base_url = "/api/units"

def get_unit(unit_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.get("{}{}/{}".format(api_url, base_url, unit_id), headers=headers)

    if response.status_code == 200:
        print("\nUnità trovata! - Status Code: {}".format(response.status_code))
        return deserialize_ingredient_unit(response.json())
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def get_all_units(api_url=mealie_url, token=api_token):
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
        return [deserialize_ingredient_unit(i) for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def search_unit(query, api_url=mealie_url, token=api_token):
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
        return [deserialize_ingredient_unit(i) for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def delete_unit(unit_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.delete(
        "{}{}/{}".format(api_url, base_url, unit_id), headers=headers
    )

    if response.status_code == 200:
        print("\nEliminato {} - Status Code: {}".format(unit_id, response.status_code))
    else:
        print(
            "\nErrore in fase di eliminazione {} - Status Code: {} - Response: {}".format(
                unit_id, response.status_code, response.text
            )
        )


def create_unit(unit_name, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    data = {"name": unit_name}

    response = requests.post(
        "{}{}".format(api_url, base_url),
        data=json.dumps(data, ensure_ascii=False),
        headers=headers,
    )

    if response.status_code == 201:
        print(
            "\nUnità creata! - Status Code: {}, Response: {}".format(
                response.status_code, response.json()
            )
        )
        return deserialize_ingredient_unit(response.json())
    else:
        print(
            "\nErrore in fase di creazione! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )


def populate_unit(unit, unit_id, api_url=mealie_url, token=api_token, delete_if_failed=False):
    headers = get_headers(token)

    response = requests.put(
        "{}{}/{}".format(api_url, base_url, unit_id),
        data=unit.serialize(),
        headers=headers,
    )

    if response.status_code == 200:
        print("\nUnità popolata! - Status Code: {}".format(response.status_code))
    else:
        print(
            "\nErrore in fase di collegamento! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )
        if delete_if_failed:
            delete_unit(unit_id, api_url, api_token)


def delete_all_units(api_url=mealie_url, token=api_token):
    unit_list = get_all_units(api_url=api_url, token=token)

    for i in unit_list:
        delete_unit(i.id)