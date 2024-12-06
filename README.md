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

| Field Name               | Type     | Description                                                                                                                                                      |
|--------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                    | String   | Unique identifier for the data point.                                                                                                                            |
| `open_xpd_uuid`         | String   | Unique identifier used in the EC3 tool.                                                                                                                          |
| `date_of_issue`         | String   | The issue date of the data point in `YYYY-MM-DD` format.                                                                                                         |
| `date_validity_ends`    | String   | The validity end date in `YYYY-MM-DD` format.                                                                                                                    |
| `category`              | Object   | Details about the category, including its `id`, `name`, and `display_name`.                                                                                      |
| `ec3_notes`             | String   | Notes about the data point's usage in EC3.<br/><span style="color:Grey;"><b>Note:</b> This field is informational only and may not represent a valid EPD.</span> |
| `lca_discussion`        | Null/String | Discussion or notes related to life cycle assessment (LCA).                                                                                                      |
| `impacts`               | Object   | Impact assessment results categorized by methods (e.g., TRACI 2.1).                                                                                              |
| `resource_uses`         | Object   | Data about resource uses (currently empty).                                                                                                                      |
| `output_flows`          | Object   | Data about output flows (currently empty).                                                                                                                       |
| `program_operator`      | Object   | Information about the program operator, including `id`, `name`, and `web_domain`.                                                                                |
| `name`                  | String   | Name of the product or scenario.                                                                                                                                 |
| `description`           | String   | Description of the product or scenario.                                                                                                                          |
| `product_classes`       | Object   | Classification of the product into various categories.                                                                                                           |
| `original_ec3_link`     | String   | URL to the original data point in the EC3 tool.                                                                                                                  |
| `declared_unit`         | String   | The declared unit for the data point (e.g., `1 kg`).                                                                                                             |
| `manufacturer`          | Object   | Information about the manufacturer, including `id`, `name`, and `web_domain`.                                                                                    |
| `plant_or_group`        | Object   | Details about the plant or group, including `id` and `name`.                                                                                                     |
| `externally_verified`   | Boolean  | Indicates whether the data has been externally verified.                                                                                                         |
| `developer`             | Null/String | Developer responsible for the data point.                                                                                                                        |
| `verifier`              | Null/String | Verifier of the data point.                                                                                                                                      |
| `reviewer`              | Null/String | Reviewer of the data point.                                                                                                                                      |
| `pcr`                   | Object   | Product category rules (PCR) details, including `id` and `name`.                                                                                                 |
| `pcr_notes`             | Null/String | Notes about the PCR.                                                                                                                                             |


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
- The `impacts` field provides detailed environmental impact data by life cycle stage.
- Use the `original_ec3_link` to view the data in the EC3 tool.

--- 

This documentation provides a comprehensive view of the JSON fields accessible via the API, ensuring easy integration and understanding of the data structure.
