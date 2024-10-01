import requests
import json
proxies = {
   'http': 'http://localhost:8080',
}
tenant_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
url="https://api.azrbac.mspim.azure.com/api/v2/privilegedAccess/aadroles/resources/"+tenant_id+"/roleDefinitions?`$select=id,displayName,type,templateId,resourceId,externalId,isbuiltIn,subjectCount,eligibleAssignmentCount,activeAssignmentCount&`$orderby=displayName"



accesstoken="eyJ0e........g"
Headers = {
    'Authorization' : 'Bearer ' + accesstoken,
    'Content-Type': 'application/json'
    }

initial_response = requests.get(url, headers=Headers,proxies=proxies)
data = initial_response.json()
roles = data.get('value', [])


# Extract role IDs
roles = data.get('value', [])



# Initialize the data structure
output = {
    "data": [],
    "meta": {
        "type": "azure",
        "version": 5,
        "count": 4850
    }
}

# Iterate through each role
for role in roles:
    role_id = role.get('id', 'N/A')
    display_name = role.get('displayName', 'N/A')
    print(f'ID: {role_id}, Display Name: {display_name}')
    
    # Construct the URL with role ID and tenant ID
    url = (
        "https://api.azrbac.mspim.azure.com/api/v2/privilegedAccess/aadroles/roleAssignments"
        "?$expand=linkedEligibleRoleAssignment,subject,scopedResource,roleDefinition($expand=resource)"
        f"&$count=true&$filter=(roleDefinition/resource/id%20eq%20%27{tenant_id}%27)"
        f"+and+(roleDefinition/id%20eq%20%27{role_id}%27)+and+(assignmentState%20eq%20%27Eligible%27)"
        "&$orderby=roleDefinition/displayName&$skip=0&$top=100"
    )
    
    try:
        # Send the GET request
        response = requests.get(url, headers=Headers, proxies=proxies)
        response.raise_for_status()  # Check for request errors
        
        # Parse the JSON response
        role_assignments_data = response.json()
        print(f"Response for Role ID {role_id}: {role_assignments_data}")

        # Extract required fields from the response
        assignments = role_assignments_data.get('value', [])
        role_assignments = []
        
        for assignment in assignments:
            role_definition_id = assignment.get('roleDefinitionId', 'N/A')
            subject_id = assignment.get('subject', {}).get('id', 'N/A')
            assignment_id = assignment.get('id', 'N/A')

            role_assignments.append({
                "id": assignment_id,
                "roleDefinitionId": role_definition_id,
                "principalId": subject_id,
                "directoryScopeId": "/",
                "roleDefinition": {"id": ""},
                "directoryScope": {
                    "id": "",
                    "api": {},
                    "info": {},
                    "optionalClaims": {},
                    "parentalControlSettings": {},
                    "publicClient": {},
                    "spa": {},
                    "verifiedPublisher": {},
                    "web": {"implicitGrantSettings": {}}
                },
                "appScope": {"id": ""}
            })

        if role_assignments:
            output["data"].append({
                "kind": "AZRoleAssignment",
                "data": {
                    "roleAssignments": role_assignments,
                    "roleDefinitionId": role_id,
                    "tenantId": tenant_id
                }
            })

    except requests.RequestException as e:
        print(f"Error fetching data for role ID {role_id}: {e}")

# Print or save the JSON output
output_json = json.dumps(output, indent=4)
print(output_json)
# Optionally, write the output to a file
with open('output2.json', 'w') as f:
    f.write(output_json)
