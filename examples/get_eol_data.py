import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Get the API key from the environment
API_KEY = os.getenv("EC3_API_KEY")
BASE_URL = os.getenv("EC3_BASE_URL")

# Set the headers
headers = {"Authorization": f"Bearer {API_KEY}"}


def main():
    print("This code is used to showcase access to BRE-X project data via EC3 API.")

    print("Getting a sample datapoint")
    get_sample("ec3y49fr")

    print("Getting a list of datapoints")
    get_list()


def get_list():
    """ Get a list of datapoints """

    url = f"{BASE_URL}/epds"  # endpoint to get the data
    url += f"?page_size=250&page_number=1"  # add API page parameters
    url += f"&plant_or_group__owned_by__name__like=BREX"  # query parameters for finding BREX data
    url += f"&fields=id,open_xpd_uuid,name,product_classes"  # query parameters for returning only relevant fields

    response = requests.get(url, headers=headers)
    response_json = response.json()

    with open(f"sample_list.json", 'w', encoding='utf-8') as f:
        json.dump(response_json, f, ensure_ascii=False, indent=4)
    print(f"Saved list to JSON")


def get_sample(open_xpd_uuid):
    """ Get a sample datapoint """

    url = f"{BASE_URL}/epds/{open_xpd_uuid}"  # endpoint to get the data

    response = requests.get(url, headers=headers)
    data = response.json()

    with open(f"sample_datapoint.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved sample to JSON")


if __name__ == "__main__":
    main()
    print(f"\nDone!")
