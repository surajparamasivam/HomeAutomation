import requests
import schedule
import time
import random
from datetime import datetime, timedelta

# Home Assistant configuration
HA_URL = "http://192.168.1.139:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"

# List of lights to control
LIGHT_ENTITIES = [
    "switch.step_lights_switch_1",
    "light.office_light",
    "light.bedroom_light",
    "light.living_room_light"
]

def get_sun_times():
    # Using sunrise-sunset.org API
    # Getting times for your location (replace lat/long as needed)
    lat = "12.9682"  # Example: New York
    lng = "80.2599"
    
    try:
        response = requests.get(f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0")
        if response.status_code == 200:
            data = response.json()['results']
            sunset = datetime.fromisoformat(data['sunset'].replace('Z', '+00:00')).astimezone()
            sunrise = datetime.fromisoformat(data['sunrise'].replace('Z', '+00:00')).astimezone()
            return sunrise, sunset
        else:
            print(f"Failed to get sun times. Status code: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error getting sun times: {str(e)}")
        return None, None

def control_lights(action):
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    # Randomize the order of lights
    random_lights = LIGHT_ENTITIES.copy()
    random.shuffle(random_lights)
    
    for light in random_lights:
        try:
            payload = {
                "entity_id": light
            }
            
            if action == "on":
                url = f"{HA_URL}/api/services/homeassistant/turn_on"
            else:
                url = f"{HA_URL}/api/services/homeassistant/turn_off"
                
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                print(f"{datetime.now()}: {light} turned {action}")
                # Add random delay between switching lights (1-5 seconds)
                time.sleep(random.uniform(1, 5))
            else:
                print(f"Failed to turn {action} {light}. Status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error controlling {light}: {str(e)}")

def schedule_lights():
    sunrise, sunset = get_sun_times()
    
    if sunrise and sunset:
        # Schedule 10 minutes before sunset and sunrise
        sunset_time = (sunset - timedelta(minutes=10)).strftime("%H:%M")
        sunrise_time = (sunrise - timedelta(minutes=10)).strftime("%H:%M")
        
        # Clear existing schedule and set new times
        schedule.clear()
        schedule.every().day.at(sunset_time).do(control_lights, "on")
        schedule.every().day.at(sunrise_time).do(control_lights, "off")
        
        print(f"Scheduled lights on at {sunset_time} and off at {sunrise_time}")

def main():
    # Initial scheduling
    schedule_lights()
    
    # Reschedule every day at midnight to get updated sun times
    schedule.every().day.at("00:00").do(schedule_lights)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
