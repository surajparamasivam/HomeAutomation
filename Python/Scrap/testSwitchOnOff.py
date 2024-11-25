import requests
import json

# Home Assistant configuration
HA_URL = "http://192.168.1.139:8123"  # Replace with your HA address
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"  # Replace with your token
LIGHT_ENTITY_ID = "switch.office_ts_switch_1"  # Replace with your light entity ID

def turn_off_light():
    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    # Payload for the request
    payload = {
        "entity_id": LIGHT_ENTITY_ID
    }

    # API endpoint for services
    url = f"{HA_URL}/api/services/homeassistant/turn_off"
    print(f"Sending request to {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")


    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print(f"Successfully turned on {LIGHT_ENTITY_ID}")
        else:
            print(f"Failed to turn off light. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    turn_off_light()
