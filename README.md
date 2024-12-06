# Accessing BRE-X data
## Documentation and examples

This repository provides guidance and examples for downloading and updating the Building Re-X End-of-life data using EC3 APIs and integrating with third-party tools. It includes setup instructions, sample scripts, and helpful utilities to streamline your workflow.

---

## Features

- Download and update data via API
- View and update dat manually via EC3 web interface
- Example API scripts

---

## Getting Started

### Prerequisites

Before you begin, make sure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)

---

### Clone & Fork

1. **Fork this repository**:
   - Click the "Fork" button in the top-right corner of this page.

2. **Clone your forked repository**:
   ```bash
   git clone https://github.com/<your-username>/api-data-toolkit.git
   cd api-data-toolkit

### Setting Up Your Environment
     
1. **Set Up a Virtual Environment**:
   - Create a virtual environment in the project directory:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```

2. **Install Project Requirements**:
   - With the virtual environment activated, install all required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Create a New Environment File**:
   - Copy the example `.env.template` file as `.env` file to create your environment file:

   - Open the `.env` file and add your [EC3 API key](https://buildingtransparency.org/ec3/manage-apps/keys).
     ```plaintext
     EC3_API_KEY=your_api_key_here
     ```

---


## Getting EC3 API Key

To access the EC3 API, you need an API key. If you don't have one, you can request it by following these steps:

1. Login to your EC3 account.
2. Open the Settings menu in the top right corner.
3. Go to [API & Integrations](https://buildingtransparency.org/ec3/manage-apps)
4. Go to [API Keys](https://buildingtransparency.org/ec3/manage-apps/keys)
5. Click the `Create API key` button.
6. Give it a `Name` and select `Scope` and `Expiry` date.
7. Click the `Create` button.
8. Copy the API key and paste it in the `.env` file.

---

## Downloading data via API

You can download the data using the EC3 API. A sample script is in the `examples` folder as `get_eol_data.py`.

This script can do two actions:
1. Get the list of IDs for all BREX data in EC3.
2. Download the complete data for each ID.

If you wanted to downlaod the data for all of the listed IDs from step 1. you can add a new function that runs step 2. in a loop for all IDs.

---

## Adding data via API

You can add the data using the EC3 API. A sample script is in the `src` folder as `bulk_import.py`.

This script loads the attached XLSX file and uploads the data to EC3. The XLSX file should be in the same format as the one attached. The script loops through each row in the XLSX file and uploads the data to EC3 according to the predefined format.

---

## Accessing data manually via EC3

You can also access the data manually via the EC3 web interface. Here are the steps to access the data:

1. Login to your EC3 account.
2. Go to [Manage Data / Product EPDs](https://buildingtransparency.org/ec3/epds)
3. Filter for data where `Manufacturer` is "BREX" as shown below
4. You can view each digital page by clicking the `Open` button.

![2024-12-05 18_02_55-.png](assets/2024-12-05%2018_02_55-.png)

---

# Fields Documentation

This section provides detailed documentation of the fields accessible via the API in a JSON format. Each field is explained along with its type and purpose.


### Top-Level Fields

| Field Name               | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                    | String   | Unique identifier for the data point.                                                                                                                                                                                                                                                                                                                                                                              |
| `open_xpd_uuid`         | String   | Unique identifier used in the EC3 tool.                                                                                                                                                                                                                                                                                                                                                                            |
| `original_ec3_link`     | String   | URL to the original data point in the EC3 tool.                                                                                                                                                                                                                                                                                                                                                                    |
| `name`                  | String   | Name of the EOL scenario.                                                                                                                                                                                                                                                                                                                                                                                          |
| `description`           | String   | Description of the EOL scenario.                                                                                                                                                                                                                                                                                                                                                                                   |
| `product_classes`       | Object   | Classification of the datapoint into various additional categories.                                                                                                                                                                                                                                                                                                                                                |
| `declared_unit`         | String   | The declared unit for the data point (e.g., `1 kg`).                                                                                                                                                                                                                                                                                                                                                               |
| `lca_discussion`        | String | Discussion or notes related to life cycle assessment (LCA), including data sources and validation information.                                                                                                                                                                                                                                                                                                     |
| `impacts`               | Object   | Impact assessment results categorized by methods (e.g., TRACI 2.1).                                                                                                                                                                                                                                                                                                                                                |
| `resource_uses`         | Object   | Data about resource uses (currently empty).                                                                                                                                                                                                                                                                                                                                                                        |
| `output_flows`          | Object   | Data about output flows (currently empty).                                                                                                                                                                                                                                                                                                                                                                         |
| `manufacturer`          | Object   | Information about the manufacturer, including `id`, `name`, and `web_domain`. <br/><span style="color:Grey;"><b>Note:</b> This is an interim use of the manufacturer field and is used for listing only relevant data in the `get_list` API function, i.e., to find only the EOL data related to this project, you can filter for the condition where `manufacturer` is `BREX`.</span>                             |
| `program_operator`      | Object   | Information about the program operator, including `id`, `name`, and `web_domain` <br/><span style="color:Grey;"><b>Note:</b> This is an interim use of the program_operator field, which automatically gives NREL staff with `manage` permissions to be able to fully [manage this data](https://docs.buildingtransparency.org/ec3/managing-data).</span>.                                                         |
| `plant_or_group`        | Object   | Details about the location where this data is available. In the current set of data, this field is set to `USA` in all cases.                                                                                                                                                                                                                                                                                      |
| `category`              | Object   | Details about the category where the EOL data is stored. In the interim all EOL data is stored under `Bulk Materials` as not to mix with other EPD data and match declared unit to mass.                                                                                                                                                                                                                           |
| `date_of_issue`         | String   | The issue date of the data point in `YYYY-MM-DD` format.                                                                                                                                                                                                                                                                                                                                                           |
| `date_validity_ends`    | String   | The validity end date in `YYYY-MM-DD` format. <br/><span style="color:Grey;"><b>Note:</b> The current data does not have an agreed upon period of validty like EPDs do and can be extended further into the future, however, if there is newer data that is published later to replace some of the existing data, this field should be used to denote the temporal boundary between the related datapoints.</span> |
| `externally_verified`   | Boolean  | Indicates whether the data has been externally verified. <br/><span style="color:Grey;"><b>Note:</b> The current dataset has not gone through external verification, but this field could communicate if this happens in the future.</span>                                                                                                                                                                        |
| `developer`             | String | Developer responsible for the data point. <b>Note:</b> Not relevant to current EOL data but could be used in the future.</span>                                                                                                                                                                                                                                                                                    |
| `verifier`              | String | Verifier of the data point. <br/><span style="color:Grey;"><b>Note:</b> Not relevant to current EOL data but could be used in the future.</span>                                                                                                                                                                                                                                                                   |
| `reviewer`              | String | Reviewer of the data point. <br/><span style="color:Grey;"><b>Note:</b> Not relevant to current EOL data but could be used in the future.</span>                                                                                                                                                                                                                                                                   |
| `pcr`                   | Object   | Product category rules (PCR) details, including `id` and `name`. <b>Note:</b> Not relevant to current EOL data but could be used in the future.</span>                                                                                                                                                                                                                                                             |


### Classification Fields

#### `product_classes`

- Contains two additional classification schemes for the data point, including:
    - `EOL Scenario` provides a detailed classification of the end-of-life scenario from the list of possible scenarios.
    - `BREX Material Category` provides a material category for which the data point is relevant.

Note: The `category` field is used to group the data points under the `Bulk Materials` EC3 category, where it is stored, and is different from which categories of materials the data is relevant to.

#### List of EOL scenarios

- `Reuse`
- `Recycling`
- `Landfill`
- `Incineration`

#### List of BREX material categories

- `Aluminium (Billet)`
- `Asphalt Shingles`
- `Concrete`
- `Fiberglass Insulation`
- `Glass`
- `Gypsum Drywall`
- `Steel`
- `Timber (CLT)`
- `Timber (Glulam)`
- `Untreated Wood`
- `Dimensional Lumber`

### Detailed Field Breakdown

#### `category`
| Field Name      | Type   | Description                      |
|-----------------|--------|----------------------------------|
| `id`           | String | Unique identifier for the category. |
| `name`         | String | Internal name of the category.   |
| `display_name` | String | Human-readable name of the category. |

#### `impacts`
- Contains impact assessment results categorized by the method name (e.g., `TRACI 2.1`).
- Each method includes categories such as `gwp` (global warming potential), broken into stages (e.g., `C1`, `C2`, `C4`, etc.).

| Field Name  | Type   | Description                                          |
|-------------|--------|------------------------------------------------------|
| `mean`     | Float  | Mean value of the impact in the declared unit.        |
| `unit`     | String | Unit of measurement (e.g., `kgCO2e`).                |
| `rsd`      | Null/Float | Relative standard deviation (if available).       |
| `dist`     | String | Distribution type (e.g., `log-normal`).               |

- If you need to access a specific impact, you need to describe the entire path to the value (e.g., `impacts['TRACI 2.1']['gwp']['C4']['mean']`).

Example JSON structure of impacts:
```json
{
    "impacts": {
        "TRACI 2.1": {
            "gwp": {
                "C1": {
                    "mean": 0.0,
                    "unit": "kgCO2e"
                },
                "C2": {
                    "mean": 0.0,
                    "unit": "kgCO2e"
                },
                "C3": {
                    "mean": 0.0,
                    "unit": "kgCO2e"
                },
                "C4": {
                    "mean": 0.0,
                    "unit": "kgCO2e"
                }
            }
        }
    }
}
```

#### `program_operator`
| Field Name   | Type   | Description                         |
|--------------|--------|-------------------------------------|
| `id`        | String | Unique identifier for the program operator. |
| `name`      | String | Name of the program operator.       |
| `web_domain` | String | Website domain of the program operator. |

#### `manufacturer`
| Field Name   | Type   | Description                           |
|--------------|--------|---------------------------------------|
| `id`        | String | Unique identifier for the manufacturer. |
| `name`      | String | Name of the manufacturer.             |
| `web_domain` | String | Website domain of the manufacturer.  |


### Notes

- Fields marked as `null` indicate the value is currently unavailable.
- The `product_classes` field provides additional classification data.
- The `impacts` field provides detailed environmental impact data by life cycle stage.
- Use the `original_ec3_link` to view the data in the EC3 tool.

--- 

This documentation provides a comprehensive view of the JSON fields accessible via the API, ensuring easy integration and understanding of the data structure.
