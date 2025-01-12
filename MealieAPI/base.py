import requests

api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb25nX3Rva2VuIjp0cnVlLCJpZCI6ImMzMzhkM2YxLTBlNjUtNGYzZS1hNDUyLTMyN2JkYzhmZGZkNSIsIm5hbWUiOiJHaWFsbG9aYWZmZXJhbm9TY3JhcGVyIiwiaW50ZWdyYXRpb25faWQiOiJnZW5lcmljIiwiZXhwIjoxODk0MjAxOTA4fQ.zEQjUJof1j3GwhqFZ39KiYKRmail3NPg9uqK_k7PHRo"
mealie_url = "http://192.168.1.26:9925"


def get_headers(token=mealie_url):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    return headers


def get_user_self(api_url=mealie_url, token=api_token):
    print("\nConnessione a Mealie...")

    headers = get_headers(token)

    response = requests.get("{}/api/users/self".format(api_url), headers=headers)

    if response.status_code == 200:
        print("\nConnessione stabilita! - Status Code: {}".format(response.status_code))
        return response.json()
    else:
        print(
            "\nErrore in fase di collegamento! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )
