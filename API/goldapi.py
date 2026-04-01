import requests

def make_gapi_request():
    api_key = "goldapi-bg14smmslcrg6-io"
    symbol = "XAU"
    curr = "CAD"
    date = "/20260310"

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"
    
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.text
        print(result)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

make_gapi_request()