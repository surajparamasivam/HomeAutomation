import requests
import schedule
import time
from datetime import datetime

# Home Assistant API configuration
HA_URL = "http://192.168.1.139:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"

# List of child lock switches to monitor
CHILD_LOCK_SWITCHES = [
    "switch.office_ts_child_lock",  # Replace with your actual switch entity IDs
    "switch.bedroom_ts_child_lock",
    "switch.living_ts1_child_lock",
    "switch.parking_ts_right_child_lock",
    "switch.parking_ts_left_child_lock",
    "switch.living_ts2_child_lock"
]

def check_and_enable_locks():
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    for switch_id in CHILD_LOCK_SWITCHES:
        try:
            # Check switch state
            state_url = f"{HA_URL}/api/states/{switch_id}"
            state_response = requests.get(state_url, headers=headers)
            
            if state_response.status_code == 200:
                switch_state = state_response.json()['state']
                
                if switch_state == 'off':
                    # Turn on the switch if it's off
                    payload = {
                        "entity_id": switch_id
                    }
                    url = f"{HA_URL}/api/services/homeassistant/turn_on"
                    
                    response = requests.post(url, headers=headers, json=payload)
                    if response.status_code == 200:
                        print(f"{datetime.now()}: {switch_id} was off, turned it on")
                    else:
                        print(f"{datetime.now()}: Failed to turn on {switch_id}. Status code: {response.status_code}")
                else:
                    print(f"{datetime.now()}: {switch_id} is already on")
            else:
                print(f"{datetime.now()}: Failed to get state for {switch_id}. Status code: {state_response.status_code}")
                
        except Exception as e:
            print(f"{datetime.now()}: Error checking {switch_id}: {str(e)}")

def main():
    # Run immediately on startup
    check_and_enable_locks()
    
    # Schedule to run every 6 hours
    schedule.every(6).hours.do(check_and_enable_locks)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
