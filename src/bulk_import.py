
"""
This script is used to import the NREL BREX EOL data into EC3 in bulk.

The script takes in tabular data from the NREL team and creates EPD-like datapoints in EC3.
"""

import os
import sys
import json
import time
import random
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

payload_cache = {}  # Cache for payloads
date_stamp = datetime.today().strftime('%y%m%d')  # Date stamp for the file

# Get the API key from the environment
API_KEY = os.getenv("EC3_API_KEY")
BASE_URL = os.getenv("EC3_BASE_URL")

# Set the headers
headers = {"Authorization": f"Bearer {API_KEY}"}


def main():
    """ Create data from table """
    filepath = os.path.join(f"brex_eol_241202.xlsx")
    df = pd.read_excel(filepath, sheet_name="Sheet1", skiprows=0)
    create_brex_data(df, filepath)


def create_brex_data(table, filepath):
    for index, row in table.iterrows():
        if pd.isnull(row["declared_unit"]):
            print(f'{index + 1} | Declared unit is missing. Skipping.')
            continue

        # if new_uuid is null, create the object and add the new_uuid to the table
        if pd.isnull(row["new_uuid"]):
            # pause for a random amount of time
            time.sleep(random.randrange(2))

            # create new object
            # Get payload from Base EPD
            payload = get_payload(row['base_uuid'])
            print(f'\n{index + 1} | Creating object.')

            lca_discussion = (
                f"# Data sources"
                f"\n*This is a datapoint describing specific EOL disposal scenario intended to be "
                f"used within a whole-life carbon assessment instead of EPD's own EOL results. "
                f"The intent behind this data is to use consistent assumptions in the estimation "
                f"of EOL impacts for materials of "
                f"the same class.*"
                f"\n\n## C1"
                f"\n*{row['source_c1']}.*"
                f"\n\n## C2"
                f"\n*{row['source_c2']}.*"
                f"\n\n## C3"
                f"\n*{row['source_c3']}.*"
                f"\n\n## C4"
                f"\n*{row['source_c4']}*"
                f"\n\n# Validation statement"
                f"\nThe following data has been obtained from other sources for validation purposes:"
                f"\n*{row['validation_statement']}*"
            )

            payload['product_classes'] = {
                "EOL Scenario": [row['eol_scenario']],
                "BREX Material Category": [row['brex_material_category']]
            }
            payload["name"] = f"{row['brex_material_category']}, {row['eol_scenario']}"
            payload['description'] = row['description']
            payload['lca_discussion'] = lca_discussion

            payload["impacts"] = {
                "TRACI 2.1": {
                    "gwp": {
                        "A1A2A3": {
                            # EC3 has a validation where this needs to be present
                            # in the current implementation this is a placeholder non-zero but very small value
                            # to get around the validator.
                            "mean": 1e-10,
                            "unit": "kgCO2e"
                        },
                        # Below is where the real C-stage data is loaded
                        "C1": {
                            "mean": row['gwp_c1'] if not pd.isnull(row['gwp_c1']) else None,
                            "unit": "kgCO2e"
                        },
                        "C2": {
                            "mean": row['gwp_c2'] if not pd.isnull(row['gwp_c2']) else None,
                            "unit": "kgCO2e"
                        },
                        "C3": {
                            "mean": row['gwp_c3'] if not pd.isnull(row['gwp_c3']) else None,
                            "unit": "kgCO2e"
                        },
                        "C4": {
                            "mean": row['gwp_c4'] if not pd.isnull(row['gwp_c4']) else None,
                            "unit": "kgCO2e"
                        }
                    }
                }
            }

            # Create the EPD with the payload
            new_url = f"https://buildingtransparency.org/api/epds"
            new_response = requests.post(new_url, headers=headers, json=payload)
            print(f"\t\tResponse status code: {new_response.status_code}")
            new_parsed_response = new_response.json() if new_response.content else None

            new_uuid = new_parsed_response.get("open_xpd_uuid")
            new_link = new_parsed_response.get("original_ec3_link")
            print(f'\t\tCreated {new_uuid} | {new_link}')

            # Update the new_uuid column and save back to Excel
            table.at[index, 'new_uuid'] = new_uuid
            table.at[index, 'link'] = new_link
            table.to_excel(filepath, sheet_name="Sheet1", index=False)

        # If new_uuid is not null, skip
        else:
            print(f'{index+1} | {row["new_uuid"]} already created. Skipping.')
            continue

    # Resave the Excel file again just in case
    table.to_excel(filepath, sheet_name="Sheet1", index=False)
    print(f"Updated Excel file: {filepath}")

    return None


def get_payload(open_xpd_uuid):
    # If in cache, retrieve the cached payload
    if open_xpd_uuid in payload_cache:
        return payload_cache[open_xpd_uuid]

    # If not cached, retrieve and cache the payload
    url = f"https://buildingtransparency.org/api/epds/{open_xpd_uuid}"
    response = requests.get(url, headers=headers)
    print(f"\t\tResponse status code: {response.status_code}")
    payload = response.json()

    attributes_to_copy = ['category', 'manufacturer', 'plant_or_group', 'pcr', 'program_operator']
    copy_dict = {}
    for attribute in attributes_to_copy:
        copy_dict[attribute] = payload[attribute]['id']
        print(f"\t\t\t{payload[attribute]['id']}")

    # Remove select data from the base payload
    attributes_to_remove = ["id", "category", "open_xpd_uuid", "created_on", "created_by", "impacts"]
    for attribute in attributes_to_remove:
        del payload[attribute]

    # Add new data to the payload
    payload['category_id'] = copy_dict['category']
    payload['manufacturer_id'] = copy_dict['manufacturer']
    payload['plant_or_group_id'] = copy_dict['plant_or_group']
    payload['program_operator_id'] = copy_dict['program_operator']
    payload['pcr_id'] = copy_dict['pcr']

    payload_cache[open_xpd_uuid] = payload
    print(f"\nCached {open_xpd_uuid}")

    return payload


if __name__ == "__main__":
    main()
