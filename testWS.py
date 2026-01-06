import requests
import json
import schedule
import time

def turn_on_samsung_tv():
    HA_URL = "http://192.168.1.139:8123"
    HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
    url = f"{HA_URL}/api/services/media_player/turn_on"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "entity_id": "media_player.samsung_cu7700_75_2"  # Updated entity ID
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Successfully turned on Samsung TV")
        else:
            print(f"Failed to turn on TV. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error turning on Samsung TV: {str(e)}")


def get_tv_state():
    HA_URL = "http://192.168.1.139:8123"
    HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
    url = f"{HA_URL}/api/states/media_player.samsung_cu7700_75_2"  # Updated entity ID
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            state_data = response.json()
            print(f"TV State: {state_data['state']}")
            print(f"Additional attributes: {json.dumps(state_data['attributes'], indent=2)}")
        else:
            print(f"Failed to get TV state. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error getting TV state: {str(e)}")


def check_tv_integration():
    HA_URL = "http://192.168.1.139:8123"
    HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    
    # Check TV state
    tv_url = f"{HA_URL}/api/states/media_player.samsung_cu7700_75_2"  # Updated entity ID
    try:
        response = requests.get(tv_url, headers=headers)
        if response.status_code == 200:
            state_data = response.json()
            print("\nTV Entity State:")
            print(f"State: {state_data['state']}")
            print(f"All Attributes: {json.dumps(state_data['attributes'], indent=2)}")
            print(f"Last Updated: {state_data.get('last_updated', 'N/A')}")
            print(f"Last Changed: {state_data.get('last_changed', 'N/A')}")
        else:
            print(f"\nFailed to get TV state. Status code: {response.status_code}")
    except Exception as e:
        print(f"\nError getting TV state: {str(e)}")
    
    # Check available media players
    entities_url = f"{HA_URL}/api/states"
    try:
        response = requests.get(entities_url, headers=headers)
        if response.status_code == 200:
            entities = response.json()
            print("\nAvailable Media Players:")
            for entity in entities:
                if entity['entity_id'].startswith('media_player.'):
                    print(f"\nEntity ID: {entity['entity_id']}")
                    print(f"State: {entity['state']}")
                    print(f"Attributes: {json.dumps(entity['attributes'], indent=2)}")
        else:
            print(f"\nFailed to get entities. Status code: {response.status_code}")
    except Exception as e:
        print(f"\nError getting entities: {str(e)}")


def turn_off_samsung_tv():
    HA_URL = "http://192.168.1.139:8123"
    HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
    url = f"{HA_URL}/api/services/media_player/turn_off"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "entity_id": "media_player.samsung_cu7700_75_2"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Successfully turned off Samsung TV")
        else:
            print(f"Failed to turn off TV. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error turning off Samsung TV: {str(e)}")

def set_tv_volume(volume_level):
    if not 0 <= volume_level <= 1:
        print("Volume must be between 0 and 1")
        return
        
    HA_URL = "http://192.168.1.139:8123"
    HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
    url = f"{HA_URL}/api/services/media_player/volume_set"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "entity_id": "media_player.samsung_cu7700_75_2",
        "volume_level": volume_level
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Successfully set TV volume to {int(volume_level * 100)}%")
        else:
            print(f"Failed to set TV volume. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error setting TV volume: {str(e)}")

def select_tv_source(source):
    HA_URL = "http://192.168.1.139:8123"
    HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
    url = f"{HA_URL}/api/services/media_player/select_source"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "entity_id": "media_player.samsung_cu7700_75_2",
        "source": source
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Successfully switched TV source to {source}")
        else:
            print(f"Failed to switch TV source. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error switching TV source: {str(e)}")

def test_tv_controls():
    print("\nTesting TV Controls:")
    
    print("\n1. Getting current TV state:")
    get_tv_state()
    time.sleep(2)
    
    print("\n2. Setting TV volume to 20%:")
    set_tv_volume(0.20)
    time.sleep(2)
    
    print("\n3. Switching to TV source:")
    select_tv_source("TV")
    time.sleep(2)
    
    print("\n4. Getting final TV state:")
    get_tv_state()

if __name__ == "__main__":
    test_tv_controls()