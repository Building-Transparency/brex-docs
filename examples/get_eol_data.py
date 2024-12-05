import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EC3_API_KEY")
BASE_URL = os.getenv("EC3_BASE_URL")

def main():
    print("This code is used to showcase access to BRE-X project data via EC3 API.")


def get_payload(base_uuid):
    url = f"https://buildingtransparency.org/api/epds/{base_uuid}"
    response = requests.get(url)
    response_json = response.json()
    return response_json


if __name__ == "__main__":
    main()
    get_payload("ec3zzn4a")
    print(f"\nDone!")
