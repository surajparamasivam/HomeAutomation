# GetDetailsEntities.py
import requests
import json

# Home Assistant API configuration
HASS_URL = "http://192.168.1.139:8123"  # Replace with your HA URL
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"  # Replace with your token

# Headers for authentication
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "content-type": "application/json",
}

def get_all_entities():
    try:
        # Make API request to get states
        response = requests.get(f"{HASS_URL}/api/states", headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            entities = response.json()
            
            # Extract entity names and their friendly names
            entity_info = []
            for entity in entities:
                entity_id = entity['entity_id']
                friendly_name = entity['attributes'].get('friendly_name', entity_id)
                entity_info.append({
                    'entity_id': entity_id,
                    'friendly_name': friendly_name
                })
            
            return entity_info
        else:
            print(f"Error: Unable to fetch entities. Status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Home Assistant: {e}")
        return None

if __name__ == "__main__":
    # Get and display all entities
    entities = get_all_entities()
    if entities:
        print("Found entities:")
        for entity in entities:
            print(f"Entity ID: {entity['entity_id']}")
            print(f"Friendly Name: {entity['friendly_name']}")
            print("-" * 50)
