import requests
import json
import schedule
import time
from datetime import datetime

# Home Assistant configuration
HA_URL = "http://192.168.1.139:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
LIGHT_ENTITY_ID = "switch.step_lights_switch_3"  # Replace with your stair light entity ID

def check_and_turn_on_light():
    # Only run between 9 PM and 6 AM
    current_hour = datetime.now().hour
    if current_hour < 21 and current_hour > 6:
        return

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    # First check light state
    try:
        state_url = f"{HA_URL}/api/states/{LIGHT_ENTITY_ID}"
        state_response = requests.get(state_url, headers=headers)
        
        if state_response.status_code == 200:
            light_state = state_response.json()['state']
            
            # If light is off, turn it on
            # Only proceed if between 9 PM and 6 AM
            current_hour = datetime.now().hour
            if not (current_hour >= 21 or current_hour < 6):
                print(f"Outside night hours (9 PM - 6 AM), skipping light check")
                return
            if light_state == 'off':
                
                payload = {
                    "entity_id": LIGHT_ENTITY_ID
                }
                url = f"{HA_URL}/api/services/homeassistant/turn_on"
                
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    print(f"Light {LIGHT_ENTITY_ID} was off, turned it on")
                else:
                    print(f"Failed to turn on light. Status code: {response.status_code}")
            else:
                print(f"Light {LIGHT_ENTITY_ID} is already on")

        else:
            print(f"Failed to get light state. Status code: {state_response.status_code}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    # Schedule the check to run every 10 minutes
    schedule.every(1).minutes.do(check_and_turn_on_light)
    
    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
