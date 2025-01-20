import requests
import schedule
import time
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configuration
HA_URL = "http://192.168.1.139:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
TV_ENTITY_ID = "media_player.samsung_cu7700_75"  # Replace with your TV entity ID

# Spotify Configuration
SPOTIFY_CLIENT_ID = '03f5bae7bf764fbebbf86ce68b2586d4'
SPOTIFY_CLIENT_SECRET = 'a3e55db8727d4f75b76d8eef90233922'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
PLAYLIST_URI = 'spotify:playlist:023ZDpHY9o4NUaHjrqqEow?si=DyEYz4v1T1aXlrG2Ch54Jg'  # Replace with your playlist URI

def setup_spotify():
    scope = "user-read-playback-state user-modify-playback-state"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope
    ))

def turn_on_tv_and_play_music():
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        # Turn on TV
        payload = {
            "entity_id": TV_ENTITY_ID
        }
        tv_url = f"{HA_URL}/api/services/media_player/turn_on"
        response = requests.post(tv_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"Failed to turn on TV. Status code: {response.status_code}")
            return
        else:
            print(f"{datetime.now()}: Successfully turned on TV")

        # Wait for TV to fully turn on
        time.sleep(20)

        # Switch to Spotify source
        payload = {
            "entity_id": TV_ENTITY_ID,
            "source": "Spotify"
        }
        source_url = f"{HA_URL}/api/services/media_player/select_source"
        response = requests.post(source_url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Failed to switch to Spotify. Status code: {response.status_code}")
            return
        else:
            print(f"{datetime.now()}: Successfully switched to Spotify")

        # Initialize Spotify
        sp = setup_spotify()
        
        # Get available devices
        devices = sp.devices()
        tv_device = next((d for d in devices['devices'] if 'Samsung' in d['name']), None)
        
        if tv_device:
            # Start playlist on TV
            sp.start_playback(device_id=tv_device['id'], context_uri=PLAYLIST_URI)
            print(f"{datetime.now()}: Successfully started morning music routine")
        else:
            print("Samsung TV not found in available Spotify devices")

    except Exception as e:
        print(f"Error in morning music routine: {str(e)}")

def main():
    # Schedule to run at 7 AM every day
    schedule.every().day.at("23:16").do(turn_on_tv_and_play_music)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
