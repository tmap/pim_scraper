# Azure PIM Role Assignment Scraper

## Overview
This Python script interacts with the Azure Role-Based Access Control (RBAC) API to retrieve role definitions and their associated PIM role assignments for a specific tenant. It is designed for red-blue-purple teamers in order to then import into Bloodhound and use this to limit ways for hackers to come in.

## Features
- Fetches role definitions for a specified Azure tenant.
- Retrieves eligible role assignments linked to each role definition.
- Outputs the data in a structured Bloodhiund JSON format.
- Supports proxy configuration for network requests.

## Prerequisites
- Python 3.x
- `requests` library (install via `pip install requests`)
- Valid Azure AD access token with the required permissions to access the RBAC API.

## Configuration
1. **Set the Proxy**: If you need to route your requests through a proxy, modify the `proxies` dictionary:
   ```python
   proxies = {
       'http': 'http://localhost:8080',
   }
2. **Tenant ID**: Replace xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx with your Azure tenant ID:
   ```python
   tenant_id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

3. **Access Token**: Replace eyJ0e........g with a valid Azure AD access token:
   ```python
   accesstoken = "eyJ0e........g"
## Usage
1. Clone this repository or download the script.
2. Open the script in your preferred Python environment.
3. Make sure you have the required configurations set.
4. Run the script:
   ```bash
   python pim_scraper.py
## Output
   ```{
    "data": [
        {
            "kind": "AZRoleAssignment",
            "data": {
                "roleAssignments": [
                    {
                        "id": "assignment_id",
                        "roleDefinitionId": "role_definition_id",
                        "principalId": "subject_id",
                        "directoryScopeId": "/",
                        ...
                    }
                ],
                "roleDefinitionId": "role_id",
                "tenantId": "tenant_id"
            }
        }
    ],
    "meta": {
        "type": "azure",
        "version": 5,
        "count": 4850
    }
}
