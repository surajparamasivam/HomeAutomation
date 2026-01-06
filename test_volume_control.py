import requests
import time

def test_volume_control():
    tv_entity = "media_player.samsung_cu7700_75_2"
    ha_url = "http://192.168.1.139:8123"
    ha_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"

    def set_volume(volume_level):
        headers = {
            "Authorization": f"Bearer {ha_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "entity_id": tv_entity,
            "volume_level": volume_level
        }
        url = f"{ha_url}/api/services/media_player/volume_set"
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f"Successfully set TV volume to {int(volume_level * 100)}%")
            else:
                print(f"Failed to set TV volume. Status code: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error setting TV volume: {str(e)}")
            return False

    # First, check if we can get the TV state
    headers = {
        "Authorization": f"Bearer {ha_token}",
    }
    try:
        response = requests.get(f"{ha_url}/api/states/{tv_entity}", headers=headers)
        if response.status_code != 200:
            print(f"Error: Cannot access TV entity. Status code: {response.status_code}")
            return
        print("Successfully connected to Home Assistant and found TV entity")
    except Exception as e:
        print(f"Error connecting to Home Assistant: {str(e)}")
        return

    # Test volume sequence
    print("\nTesting volume sequence:")
    print("1. Setting initial volume to 18%...")
    if not set_volume(0.18):
        return

    print("\nVolume will increase to 20% in 5 seconds (simulating 30 minutes)...")
    time.sleep(5)
    if not set_volume(0.20):
        return

    print("\nVolume will increase to 22% in 5 seconds (simulating 1 hour)...")
    time.sleep(5)
    if not set_volume(0.22):
        return

    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_volume_control()
