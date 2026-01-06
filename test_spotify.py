import requests
import json
import time
from pysmartthings import SmartThings

def test_youtube_playback():
    # SmartThings Configuration
    token = "YOUR_SMARTTHINGS_TOKEN"  # Replace with your SmartThings API token
    st = SmartThings(token)
    
    # Home Assistant Configuration
    ha_url = "http://192.168.1.139:8123"  # Replace with your Home Assistant URL
    ha_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"  # Your Long-Lived Access Token
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "content-type": "application/json",
    }
    
    # Device configurations
    youtube_entity = "media_player.samsung_cu7700_75"  # Update this to match your YouTube entity
    tv_device_label = "Samsung TV"  # Update this to match your TV's label in SmartThings
    video_id = "dQw4w9WgXcQ"  # Replace with your desired YouTube video ID
    
    print("Checking YouTube TV status...")
    try:
        # Get TV device from SmartThings
        devices = st.devices()
        tv_device = next((device for device in devices if device.label == tv_device_label), None)
        
        if not tv_device:
            raise Exception(f"Could not find TV device with label: {tv_device_label}")
        
        # Get current state and switch on if needed using SmartThings
        tv_status = tv_device.status()
        if not tv_status.switch:
            print("TV is off. Turning it on via SmartThings...")
            tv_device.switch_on()
            print("TV turned on successfully")
            # Wait for the TV to fully boot
            time.sleep(10)
        
        # Get current state of YouTube player from Home Assistant
        response = requests.get(
            f"{ha_url}/api/states/{youtube_entity}",
            headers=headers
        )
        response.raise_for_status()
        youtube_state = response.json()
        
        # Show current state
        print(f"\nYouTube TV Status: {youtube_state['state']}")
        
        # Turn on the device if it's off
        if youtube_state['state'] == 'off':
            print("YouTube TV is off. Turning it on...")
            response = requests.post(
                f"{ha_url}/api/services/media_player/turn_on",
                headers=headers,
                json={
                    "entity_id": youtube_entity
                }
            )
            response.raise_for_status()
            print("YouTube TV turned on successfully")
            # Wait for the device to fully turn on
            time.sleep(5)
            
        if 'attributes' in youtube_state:
            attrs = youtube_state['attributes']
            
            # Show current video if playing
            if 'media_title' in attrs:
                print(f"Currently playing: {attrs['media_title']}")
        
        # Start YouTube video playback
        print("Starting YouTube video...")
        response = requests.post(
            f"{ha_url}/api/services/media_player/play_media",
            headers=headers,
            json={
                "entity_id": youtube_entity,
                "media_content_id": video_id,
                "media_content_type": "youtube"
            }
        )
        response.raise_for_status()
        print("Playback command sent successfully")
        
        # Wait a moment and show what's playing
        time.sleep(2)
        response = requests.get(
            f"{ha_url}/api/states/{youtube_entity}",
            headers=headers
        )
        youtube_state = response.json()
        if 'attributes' in youtube_state:
            attrs = youtube_state['attributes']
            if 'media_title' in attrs:
                print(f"\nNow playing: {attrs['media_title']}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Home Assistant: {str(e)}")
        return
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return

if __name__ == "__main__":
    test_youtube_playback()
