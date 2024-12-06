import os
import json
import time
import random
import requests
from datetime import datetime
from dotenv import load_dotenv


def save_json(data, directory="data", filename="unnamed_saved_json"):
    # If name includes .json remove it first
    filename = filename.replace(".json", "")

    # Check if the data is empty or invalid before attempting to save
    if not data:
        print(f"\tSkipping save for {filename}.json due to empty or invalid data.")
        return

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"\tCreated directory: {directory}\n")

    filepath = os.path.join(directory, f"{filename}.json")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\tSaved JSON to {filepath}")
    except Exception as e:
        print(f"\tError saving JSON to {filepath}: {e}")


def extract(data_point, keys):
    """Extracts a value from a nested dictionary using a list of keys."""
    value = data_point
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None  # Return None or a default value if the path doesn't exist
    return value


# fetch with throttle for single credential
def smart_crud(url, method="GET", max_retries=5, data=None, json_data=None, creds=None):
    """
    Fetch data from the given URL, handle 429 Throttling errors by waiting.

    :param url: URL to fetch data from
    :param max_retries: Maximum number of retries
    """
    # get the right headers for the instance based on url
    # the part between ""https://" and ".buildingtransparency" is the instance and if blank, it is ec3
    instance = url.split("https://")[1].split(".buildingtransparency")[0] if ".buildingtransparency" in url else "ec3"
    # print(f"Instance: {instance}")

    if creds:
        # api_key when specific credentials are provided
        api_key = os.getenv(creds)
        print(f"Using credentials: {creds}")
    else:
        # .env has the corresponding API KEY as "EC3_API_KEY"+"_"+instance.upper()
        api_key = os.getenv("EC3_API_KEY_" + instance.upper()) if instance != "ec3" else os.getenv("EC3_API_KEY")

    headers = {"Authorization": f"Bearer {api_key}"}
    # print(f"API Key: {api_key[:5]}***************")

    retries = 0
    response = None

    while retries < max_retries:
        try:
            # Choose the HTTP method dynamically
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, data=data, json=json_data)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, data=data, json=json_data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, data=data, json=json_data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)

            print(f"Response status code: {response.status_code}")

            # If the request is successful, return the response
            if response.status_code == 200:
                print(f"Data fetched successfully.")
                parsed_response = response.json() if response.content else None
                return parsed_response

            elif response.status_code == 201:
                parsed_response = response.json() if response.content else None
                print(f"Created new resource: {parsed_response}")
                return parsed_response

            elif response.status_code == 204:
                print(f"Resource deleted successfully.")
                return response.status_code

            # Handle 429 Throttling Error
            elif response.status_code == 429:
                error_data = json.loads(response.content)
                wait_time = error_data.get('detail')

                if "Expected available in" in wait_time:
                    wait_seconds = int(wait_time.split()[-2]) + 1  # Extract the number before "seconds."
                    print(f"\nThrottled on API key for {instance}. Waiting {wait_seconds} seconds.\n")
                    time.sleep(wait_seconds)
                else:
                    print(f"Throttled. Waiting for 60 seconds (default).\n")
                    time.sleep(60)

                retries += 1

            else:
                print(f"Error: Received status code {response.status_code}\n{response.content}")
                return response.status_code

        except requests.exceptions.RequestException as e:
            print(f"Request failed due to an exception: {e}\n")
            retries += 1
            time.sleep(2 ** retries)

    print(f"Failed to {method} data from {url} after {max_retries} retries.\n")
    return None
