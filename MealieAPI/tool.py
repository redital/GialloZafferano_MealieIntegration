import requests
import json
from MealieAPI.base import * 
from MealieAPI.deserialize_models import deserialize_recipe_tool

base_url = "/api/organizers/tools"

def get_tool(tool_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.get("{}{}/{}".format(api_url, base_url, tool_id), headers=headers)

    if response.status_code == 200:
        print("\nStrumento trovato! - Status Code: {}".format(response.status_code))
        return deserialize_recipe_tool(response.json())
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def get_all_tools(api_url=mealie_url, token=api_token):
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
        return [deserialize_recipe_tool(i) for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def search_tool(query, api_url=mealie_url, token=api_token):
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
        return [deserialize_recipe_tool(i) for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def delete_tool(tool_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.delete(
        "{}{}/{}".format(api_url, base_url, tool_id), headers=headers
    )

    if response.status_code == 200:
        print("\nEliminato {} - Status Code: {}".format(tool_id, response.status_code))
    else:
        print(
            "\nErrore in fase di eliminazione {} - Status Code: {} - Response: {}".format(
                tool_id, response.status_code, response.text
            )
        )


def create_tool(tool_name, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    data = {"name": tool_name}

    response = requests.post(
        "{}{}".format(api_url, base_url),
        data=json.dumps(data, ensure_ascii=False),
        headers=headers,
    )

    if response.status_code == 201:
        print(
            "\nStrumento creato! - Status Code: {}, Response: {}".format(
                response.status_code, response.json()
            )
        )
        return deserialize_recipe_tool(response.json())
    else:
        print(
            "\nErrore in fase di creazione! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )


def populate_tool(tool, tool_id, api_url=mealie_url, token=api_token, delete_if_failed=False):
    headers = get_headers(token)

    response = requests.put(
        "{}{}/{}".format(api_url, base_url, tool_id),
        data=tool.serialize(),
        headers=headers,
    )

    if response.status_code == 200:
        print("\nStrumento popolato! - Status Code: {}".format(response.status_code))
    else:
        print(
            "\nErrore in fase di collegamento! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )
        if delete_if_failed:
            delete_tool(tool_id, api_url, api_token)


def delete_all_tools(api_url=mealie_url, token=api_token):
    tool_list = get_all_tools(api_url=api_url, token=token)

    for i in tool_list:
        delete_tool(i.id)